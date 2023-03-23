import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
TEST_NUMBER='++13157918467'
def send_text(alarm):
    message = client.messages.create(
                     body=alarm['message'],
                     from_=TEST_NUMBER,
                     to=alarm['phone']
                 )
    print(message.sid)

