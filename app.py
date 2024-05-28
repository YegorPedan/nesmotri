from flask import Flask, render_template, send_from_directory
from imap_tools import MailBox, AND
from secret_imap import IMAP_URL, EMAIL_LOGIN, EMAIL_PASSWORD
import sqlite3
import json

app = Flask(__name__, template_folder="www")
db_location = '/var/www/PD_Vlad/station.db'


############
# FLASK CODE
############
@app.route('/')
def main_page():  # put application's code here
    iserr = ""
    cards_background = "primary"
    try:
        with MailBox(IMAP_URL).login(EMAIL_LOGIN, EMAIL_PASSWORD, 'inbox') as mailbox:
            for msg in mailbox.fetch(AND(seen=False), reverse=True):
                temp_data = json.loads(msg.text.strip())
                temp_data = temp_data[0]
                # print("GOT IMAP MESSAGE: ", temp_data)
                save_data(temp_data)
    except Exception as e:
        iserr = f"An error occurred while connecting to the mailbox: {e}"
        cards_background = "danger"
        # print(f"An ACTUAL ERROR occurred while connecting to the mailbox: {e}")
    return render_template('index.html', phones_data=get_data(), iserr=iserr, cards_background=cards_background)


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
    # print("SAVED DATA: ", data)
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
