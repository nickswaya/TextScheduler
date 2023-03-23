# from huey import crontab
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.db import get_db
from flaskr.auth import login_required
import datetime
from huey import SqliteHuey
import time

bp = Blueprint('scheduler', __name__)

huey = SqliteHuey(filename=r'C:\Users\nicks\OneDrive\Documents\Projects\TextScheduler\var\flaskr-instance\flaskr.sqlite')

@huey.task()
def example_task(n):
    return print(n)


@bp.route('/scheduler', methods=('GET', 'POST'))
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
            
            
            
            return redirect(url_for('blog.calendar'))

    return render_template('blog/create.html')




#     @huey.periodic_task(crontab(minute='*/5'))
#     def print_every5_minutes():
#         # Example periodic task -- this runs every 5 minutes and prints the
#         # following line to the stdout of the consumer process.
#         print('-- PERIODIC TASK -- THIS RUNS EVERY 5 MINUTES --')