from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wtforms.fields import DateTimeField
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.messager import send_text

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    total_post_count = db.execute(
        'SELECT COUNT(p.id) as count'
        ' FROM post p'
    ).fetchall()[0]

    total_user_count = db.execute(
        'SELECT COUNT(u.id) as count'
        ' FROM user u'
    ).fetchall()[0]

    return render_template('blog/index.html', posts=posts, total_post_count=total_post_count, total_user_count=total_user_count)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


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
def calendar():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        error = None

        if not date:
            error = 'Date is required.'
        if not time:
            error = 'Time is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (date, time, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
   
    return render_template('blog/calendar.html')


@bp.route('/delete-all-alarms', methods=('GET', 'POST'))
def delete_all_alarms():
    print(g.user['id'])
    db = get_db()
    db.execute('DELETE FROM post WHERE author_id = ?', (g.user['id'],))
    db.commit()
    send_text({'message': 'test',
               "phone": '14255022930'})
    return redirect(url_for('blog.index'))

