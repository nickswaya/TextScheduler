from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wtforms.fields import DateTimeField
from flaskr.auth import login_required
from flaskr.db import get_db
from wtforms import Form, StringField, validators
from datetime import datetime
import datetime as dt
from flaskr.analytics import dict_from_row


bp = Blueprint('blog', __name__)

date_regex = r"^(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])\/\d{4}$"
time_regex = r"^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$"


def convert_time_12_to_24(time_string):
    """
    Takes a time string in the format of "hh:mm:ss AM/PM" and converts it to the 24-hour format "%H:%M:%S".
    """
    time_12 = dt.datetime.strptime(time_string, '%I:%M:%S %p')
    time_24 = time_12.strftime('%H:%M:%S')
    return time_24


class RegistrationForm(Form):
    date = StringField('Date', [validators.Regexp(regex=date_regex, message="Must match date format 'MM/DD/YYYY'")], description="Enter as MM/DD/YYYY")
    time = StringField('Time', [validators.Regexp(regex=time_regex, message="Must match time format 'HH/MM/SS'")])
    body = StringField('Alarm Note')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT a.id, date, time, created, author_id, username'
        ' FROM alarm a JOIN user u ON a.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    total_alarm_count = db.execute(
        'SELECT COUNT(a.id) as count'
        ' FROM alarm a'
    ).fetchall()[0]

    total_user_count = db.execute(
        'SELECT COUNT(u.id) as count'
        ' FROM user u'
    ).fetchall()[0]

    return render_template('blog/index.html', posts=posts, total_user_count=total_user_count, total_alarm_count=total_alarm_count)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT a.id, date, time, created, author_id, username, a.body'
        ' FROM alarm a JOIN user u ON a.author_id = u.id'
        ' WHERE a.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    form = RegistrationForm(request.form)
    row_dict = dict_from_row(post)
    if request.method == 'POST':
        if not form.validate():
            flash_errors(form)    
            return redirect(url_for('blog.update', form=form, last_date=row_dict['date'], last_time=row_dict['time'], last_body=row_dict['body']))
        else:
            db = get_db()
            db.execute(
                'UPDATE alarm SET date = ?, body = ?'
                ' WHERE id = ?',
                (form.date.data, form.body.data, id)
            )
            db.commit()
            flash("Alarm Updated")
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post, form=form, last_date=row_dict['date'], last_time=row_dict['time'], last_body=row_dict['body'])


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM alarm WHERE id = ?', (id,))
    db.commit()
    flash("Alarm Deleted")
    return redirect(url_for('blog.index'))


@bp.route('/calendar', methods=('GET', 'POST'))
def calendar():
    date_placeholder = datetime.strftime(datetime.now(), "%m/%d/%Y")
    time_placeholder = datetime.strftime(datetime.now(), "%H:%M:%S")
    body_placeholder = "Alarm Note to be sent"
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            flash_errors(form)    
            return redirect(url_for('blog.calendar', form=form, date_placeholder=date_placeholder, time_placeholder=time_placeholder, body_placeholder=body_placeholder))
        
        else:
            db = get_db()
            db.execute(
                'INSERT INTO alarm (date, time, author_id, body)'
                ' VALUES (?, ?, ?, ?)',
                (form.date.data, form.time.data, g.user['id'], form.body.data)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/calendar.html', form=form, date_placeholder=date_placeholder, time_placeholder=time_placeholder,body_placeholder=body_placeholder)


@bp.route('/delete-all-alarms', methods=('GET', 'POST'))
def delete_all_alarms():
    print(g.user['id'])
    db = get_db()
    db.execute('DELETE FROM alarm WHERE author_id = ?', (g.user['id'],))
    db.commit()
    flash("All Alarms Deleted")
    return redirect(url_for('blog.index'))

