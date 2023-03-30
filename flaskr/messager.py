import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
import sqlite3
import time

load_dotenv()


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
TEST_NUMBER='++13157918467'


def get_delta_seconds(date, hms):
    datetime_str = str(date) + " " + str(hms)
    return (datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S') - datetime.now()).total_seconds() // 1


def send_text(body, phone):
    message = client.messages.create(
                     body=body,
                     from_=TEST_NUMBER,
                     to=phone
                 )
    print(message.sid)

def get_db():
        db = sqlite3.connect(
            r"C:\Users\nicks\OneDrive\Documents\Projects\TextScheduler\var\flaskr-instance\flaskr.sqlite",
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False
        )
        db.row_factory = sqlite3.Row
        return db


def close_db(g=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with open(r'schema.sql') as f:
        db.executescript(f.read().decode('utf8'))



def poll_alarms():
    current_date = datetime.strftime(datetime.now(), "%m/%d/%Y")
    current_time = datetime.strftime(datetime.now(), "%H:%M:%S")

    db = get_db()

    alarms = db.execute(
        'SELECT *'
        ' FROM alarm a JOIN user u ON a.author_id = u.id'
        ' WHERE a.date = ? and a.time = ?',
        (current_date,current_time)
    ).fetchall()

    if alarms:
         for alarm in alarms:
              send_text(alarm[5], alarm[9])
    db.close()



while True:
     time.sleep(1)
     print(poll_alarms())