import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
TEST_NUMBER='++13157918467'


def get_delta_seconds(date, hms):
    datetime_str = str(date) + " " + str(hms)
    return (datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S') - datetime.now()).total_seconds() // 1


def send_text(alarm):
    message = client.messages.create(
                     body=alarm['message'],
                     from_=TEST_NUMBER,
                     to=alarm['phone']
                 )
    print(message.sid)

