import os
import time
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
from analytics import get_db, dict_from_row

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


def poll_alarms():
    db = get_db()

    current_date = datetime.strftime(datetime.now(), "%m/%d/%Y")
    current_time = datetime.strftime(datetime.now(), "%H:%M:%S")

    alarms = db.execute(
        'SELECT *'
        ' FROM alarm a JOIN user u ON a.author_id = u.id'
        ' WHERE a.date = ? and a.time = ?',
        (current_date,current_time)
    ).fetchall()

    if alarms:
         for alarm in alarms:
            alarm_dict = dict_from_row(alarm)
            send_text(alarm_dict['body'], alarm_dict['phonenumber'])
            db.execute(
            'INSERT INTO sent_messages (recipient, phonenumber)'
            ' VALUES (?,?)',
            (alarm['username'], alarm['phonenumber'],)
            )
            db.commit()
    db.close()


while True:
     time.sleep(1)
     print(poll_alarms())