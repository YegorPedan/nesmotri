from flask import Flask, render_template, send_from_directory
from paho.mqtt import client as mqtt_client
from mqtt_config_secret import MQTT_USERNAME, MQTT_PASSWORD, MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_TOPIC
from threading import Thread
import sqlite3
import random

app = Flask(__name__, template_folder="www")
db_location = 'station.db'
paho_client_id = f'webserver-{random.randint(0, 1000)}'


################
# PAHO-MQTT CODE
################
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("["+str(msg.qos)+"] "+msg.topic+" "+msg.payload.decode('utf-8'))

def run_mqtt_client():
    client = mqtt_client.Client(paho_client_id)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)
    client.loop_forever()


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
    mqtt_thread = Thread(target=run_mqtt_client)
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=5000)