import sqlite3


def get_db():
    db = sqlite3.connect(
        r".\var\flaskr-instance\flaskr.sqlite",
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False
    )
    db.row_factory = sqlite3.Row
    return db


def dict_from_row(row):
    return dict(zip(row.keys(), row))


def query_users():
    users = get_db().execute(
    'SELECT username, phonenumber'
    ' FROM user'
    ).fetchall()

    return [dict_from_row(user) for user in users]
   

def query_alarms():
    alarms = get_db().execute(
    'SELECT u.username, a.created, a.time'
    ' FROM alarm a JOIN user u ON a.author_id = u.id'
    ' ORDER BY created DESC'
    ).fetchall()

    return [dict_from_row(alarm) for alarm in alarms]


def query_sent_messages():
    sent_messages = get_db().execute(
    'SELECT *'
    ' FROM sent_messages'
    ).fetchall()

    return [dict_from_row(sent_message) for sent_message in sent_messages]


if __name__ == '__main__':
    pass