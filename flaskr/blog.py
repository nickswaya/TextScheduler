from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wtforms.fields import DateTimeField
from flaskr.auth import login_required
from flaskr.db import get_db
from wtforms import Form, StringField, validators
import re


bp = Blueprint('blog', __name__)
date_regex = r"^(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])\/\d{4}$"
time_regex = r"^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$"

class RegistrationForm(Form):
    date = StringField('Date', [validators.Regexp(regex=date_regex, message="Must match date format 'MM/DD/YYYY'")])
    time = StringField('Time', [validators.Regexp(regex=time_regex, message="Must match time format 'HH/MM/SS'")])


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
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
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

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/calendar', methods=('GET', 'POST'))
async def calendar():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            flash_errors(form)    
            return redirect(url_for('blog.calendar', form=form))
        
        else:
            db = get_db()
            db.execute(
                'INSERT INTO alarm (date, time, author_id)'
                ' VALUES (?, ?, ?)',
                (form.date.data, form.time.data, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/calendar.html', form=form)


@bp.route('/delete-all-alarms', methods=('GET', 'POST'))
def delete_all_alarms():
    print(g.user['id'])
    db = get_db()
    db.execute('DELETE FROM post WHERE author_id = ?', (g.user['id'],))
    db.commit()
    return redirect(url_for('blog.index'))

