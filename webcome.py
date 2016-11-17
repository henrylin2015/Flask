# -*-  coding: utf-8 -*-
# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
import pymysql
host = '127.0.0.1'
user = 'root'
password = ''
db = 'flask'
port = 3306
charset = 'utf8'

app = Flask(__name__)


def connect_db():
    """Connects to the specific database."""
    # rv = sqlite3.connect(app.config['DATABASE'])
    # rv = sqlite3.connect('test')
    # rv.row_factory = sqlite3.Row
    # return rv
    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db,
                               charset=charset, port=port)
        cur = conn.cursor()
        return (conn, cur)
    except Exception as e:
        print("Error:", e)
        return


# 关闭所有连接
def connClose(cnn, cur):
    if cur:
        cur.close()
    if cnn:
        cnn.close()


@app.route('/')
def show_entries():
    conn, cur = connect_db()
    cur.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    print(entries)
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(port='5001')
