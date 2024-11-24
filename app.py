from flask import Flask, render_template, send_from_directory, redirect
from imap_tools import MailBox, AND
import sqlite3
import re
import json
import logging

from secrept_imap import IMAP_URL, EMAIL_LOGIN, EMAIL_PASSWORD

app = Flask(__name__, template_folder="www")
db_location = './station.db'

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


############
# FLASK CODE
############
@app.route('/')
def main_page():
    iserr = ""
    cards_background = "primary"
    try:
        logging.debug("Попытка подключения к почтовому ящику")
        with MailBox(IMAP_URL).login(EMAIL_LOGIN, EMAIL_PASSWORD,
                                     initial_folder="INBOX") as mailbox:
            logging.debug("Успешное подключение к почтовому ящику")
            for msg in mailbox.fetch(reverse=True):
                try:
                    # Получаем текст сообщения
                    # pattern = r'"(\w+)":"(.*?)"'
                    pattern = r'"([^"]+)":"(.*?)"'

                    # Найдём все совпадения
                    matches = re.findall(pattern, msg.text.strip())

                    # Преобразуем список кортежей в словарь
                    s_dict = {key: value for key, value in matches}

                    logging.debug(f"Корректные данные: {s_dict}")

                    # Сохраняем данные
                    save_data(s_dict)

                except json.JSONDecodeError as jde:
                    logging.error(f"Ошибка декодирования JSON: {jde}")
                except KeyError as ke:
                    logging.error(f"Отсутствует ключ в данных: {ke}")
    except Exception as e:
        iserr = f"Произошла ошибка при подключении к почтовому ящику: {e}"
        cards_background = "danger"
        logging.error(f"Произошла ошибка при подключении к почтовому ящику: {e}")

    return render_template('index.html', phones_data=get_data(), iserr=iserr,
                           cards_background=cards_background)


@app.route('/favicon.ico')
def favicon():
    return redirect("https://mospolytech.ru/favicon.ico", code=301)


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('www/assets', path)


###########
# FUNCTIONS
###########
def save_data(data: json):
    try:
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        # First, try to insert the new record. This will do nothing if it exists.
        is_id = c.execute(f"""SELECT id FROM phone WHERE id = {data["id"]}""")
        if len(is_id) == 0:
            c.execute("""
                INSERT OR IGNORE INTO phones
                (id, name, model, charge, connection_time, disconnection_time)
                VALUES (?, ?, ?, ?, ?, ?)""", (
                data['id'],
                data['name'],
                data['model'],
                data['charge'],
                data['connection_time'],
                data['disconnection_time']
            ))
            conn.commit()
            logging.debug(f"Сохранены данные: {data}")
    except sqlite3.Error as db_err:
        logging.error(f"Ошибка базы данных: {db_err}")
    finally:
        conn.close()


def get_data():
    try:
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        c.execute('SELECT * FROM phones')
        phones_fetch = c.fetchall()
        logging.debug(f"Получены данные из базы: {phones_fetch}")
        return phones_fetch
    except sqlite3.Error as db_err:
        logging.error(f"Ошибка базы данных при получении данных: {db_err}")
        return []
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5003, debug=True)
