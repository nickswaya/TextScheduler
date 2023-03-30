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


import re

date_regex = r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-\d{4}$"
date_string = "03/30/2023"
if re.match(date_regex, date_string):
    print("Valid date")
else:
    print("Invalid date")



