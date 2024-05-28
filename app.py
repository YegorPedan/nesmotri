from flask import Flask, render_template, send_from_directory
from imap_tools import MailBox, AND
from secret_imap import IMAP_URL, EMAIL_LOGIN, EMAIL_PASSWORD
import sqlite3
import json

app = Flask(__name__, template_folder="www")
db_location = 'station.db'


############
# FLASK CODE
############
@app.route('/')
def main_page():  # put application's code here
    try:
        with MailBox(IMAP_URL).login(EMAIL_LOGIN, EMAIL_PASSWORD, 'inbox') as mailbox:
            for msg in mailbox.fetch(AND(seen=False)):
                temp_data = json.loads(msg.text.strip())
                temp_data = temp_data[0]
                # print("MESSAGE: ", temp_data)
                save_data(temp_data)
    except Exception as e:
        print(f"An error occurred while connecting to the mailbox: {e}")
    return render_template('index.html', phones_data=get_data())


@app.route('/favicon.ico')
def favicon():
    return app.redirect("https://mospolytech.ru/favicon.ico", code=301)


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('www/assets', path)


###########
# FUNCTIONS
###########
def save_data(data):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO phones VALUES (?, ?, ?, ?, ?, ?)", (
    data['id'], data['name'], data['model'], data['charge'], data['connection_time'], data['disconnection_time']))
    conn.commit()
    conn.close()


def get_data():
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute('SELECT * FROM phones')
    phones_fetch = c.fetchall()
    conn.close()
    # print("FETCHED DATA: ", phones_fetch)
    return phones_fetch


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
