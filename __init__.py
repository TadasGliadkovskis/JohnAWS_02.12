import os
from functools import wraps
from flask import Flask, render_template, redirect, session, url_for, flash
import json
import time, threading
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_sqlalchemy import SQLAlchemy
from . import myDB

app = Flask(__name__)

# password = os.getenv("MYSQL_PASSWORD")
password = "Zebras11!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:{}@localhost/iot_class'.format(password)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

facebook_id = '578340929913821'
facebook_secret = '1b273f9d33c139d3cc973380f72a8a2d'

facebook_blueprint = make_facebook_blueprint(client_id=facebook_id, client_secret=facebook_secret, redirect_url='/facebook_login')
app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')

alive = 0
data = {}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session['logged_in']:
            return f(*args, **kwargs)
        flash("Please log in first")
        return redirect(url_for('login'))

    return wrapper


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/facebook_login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    account_info = facebook.get('/me')
    if account_info.ok:
        print("Access Token: ", facebook.access_token)
        me = account_info.json()
        session['logged_in'] = True
        session['facebook_token'] = facebook.access_token
        session['user'] = me['name']
        session['user_id'] = me['id']
        return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    clear_user_session()
    flash("You just logged out")
    return redirect(url_for('login'))


@app.route('/login')
def login():
    clear_user_session()
    return render_template('login.html')


def clear_user_session():
    session['facebook_token'] = None
    session['user'] = None
    session['user_id'] = None
    session['logged_in'] = None


@app.route('/home')
@login_required
def home():
    flash(session['user'])
    myDB.userTable.add_user_and_login(session['user'], int(session['user_id']))
    return render_template("index.html")


@app.route('/keep_alive')
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    print("Got " + name + ", action: " + action)
    if name == "buzzer":
        if action == "ON":
            data["alarm"] = True
        elif action == "OFF":
            data["alarm"] = False
    return str("OK")


if __name__ == '__main__':
    app.run()
