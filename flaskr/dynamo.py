import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
import os
from flaskr.db import get_db



def poll_alarms():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    
# load_dotenv()
# access_key = os.environ['ACCESS_KEY']
# secret = os.environ['AWS_SECRET']


# client = boto3.client(
#     'dynamodb',
#     region_name='us-west-2',
#     aws_access_key_id=access_key,
#     aws_secret_access_key=secret
#     )
# dynamodb = boto3.resource(
#     'dynamodb',
#     region_name='us-west-2',
#     aws_access_key_id=access_key,
#     aws_secret_access_key=secret
#     )
# ddb_exceptions = client.exceptions


# item = {
#     "id": "1",
#     "author_id": "Nick",
#     "datetime": "2023-3-27T17:42:34Z",
#     "note": "test"
# }

# dynamodb.Table('Alarms').put_item(
#     Item=item
#         )

# response = dynamodb.Table('Alarms').query(
#     KeyConditionExpression=Key('created').eq("12:00pm")
# )
# print(response)

