from flask import Flask, render_template, send_from_directory
import sqlite3
from flask_mqtt import Mqtt
from dotenv import dotenv_values # https://blog.gitguardian.com/how-to-handle-secrets-in-python/

mqtt_variables = dotenv_values(".env")

app = Flask(__name__, template_folder="www")
db_location = 'station.db'

# flask_mqtt config
app.config['MQTT_BROKER_URL'] = mqtt_variables["MQTT_BROKER_URL"]
app.config['MQTT_BROKER_PORT'] = int(mqtt_variables["MQTT_BROKER_PORT"])
app.config['MQTT_USERNAME'] = mqtt_variables["MQTT_USERNAME"]  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = mqtt_variables["MQTT_PASSWORD"]  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = 'test'

mqtt_client = Mqtt(app)


################
# FLASK_MQTT CODE
################
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('MQTT: Connected successfully.')
        mqtt_client.subscribe(topic)  # subscribe topic
    else:
        print('MQTT: Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('MQTT: Received message on topic: {topic} with payload: {payload}'.format(**data))


############
# FLASK CODE
############
@app.route('/')
def main_page():  # put application's code here
    return render_template('index.html', phones_data=get_phones_data())


@app.route('/favicon.ico')
def favicon():
    return app.redirect("https://mospolytech.ru/favicon.ico", code=302)


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('www/assets', path)


###########
# FUNCTIONS
###########
def get_phones_data():
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute('SELECT * FROM phones')
    phones_fetch = c.fetchall()
    print(phones_fetch)

    phones_data = []
    if not phones_fetch:
        phones_data += {("NULL", "danger", "База данных пуста")}
    else:
        for row in phones_fetch:
            if row[1] == 1:
                sec = row[2]
                time = ""
                if sec >= 86400:
                    days = sec // 86400
                    time += str(days) + (
                        " день " if days % 10 == 1 else (" дня " if days % 10 >= 2 or days % 10 <= 4 else " дней "))
                    sec %= 86400
                if sec >= 3600:
                    hours = sec // 3600
                    time += str(hours) + (
                        " час " if hours % 10 == 1 else (" часа " if hours % 10 >= 2 or hours % 10 <= 4 else " часов "))
                    sec %= 3600
                if sec >= 60:
                    minutes = sec // 60
                    time += str(minutes) + " мин. "
                    sec %= 60
                if sec > 0:
                    time += str(sec) + " сек."
            else:
                time = "Пусто"
            phones_data += {(row[0], "success" if row[1] == 1 else ("secondary" if row[1] == 0 else "danger"), time)}

    print('Phones data: ', phones_data)
    return phones_data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)