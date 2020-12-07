from flask import Flask, render_template, url_for, session, flash
import json
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from functools import wraps
from . import myDB,PB
import string, random, hashlib
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:CareTrackerPassword123@localhost/CareTrackerApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

alive = 0
data = {}


# Paste in your Facebook appIOD and Secret Key
facebook_id = "744114852893612"
facebook_secret = "f67621b31d004f95689a5eeeddc9313a"

facebook_blueprint = make_facebook_blueprint(client_id=facebook_id, client_secret=facebook_secret)
app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')


PB.grant_access("IOTCA-PI", True, True)


@app.route("/facebook_login")
def facebook_login():
    if not facebook.authorized:
        print("Not authorized, redirect...")
        return redirect(url_for("facebook.login"))

    account_info = facebook.get('/me')
    if account_info.ok:
        print("Access token: ", facebook.access_token)
        me = account_info.json()
        session['logged_in'] = True
        session['facebook_token'] = facebook.access_token
        session['user'] = me['name']
        session['user_id'] = me['id']
        return redirect(url_for('main'))


def loginRequired(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            if session["logged_in"]:
                return f(*args, **kwargs)
        flash("Please login first")
        return redirect(url_for("login"))
    return wrapper


@app.route("/main")
@loginRequired
def main():
    flash(session["user"])
    myDB.add_user_and_login(session['user'], int(session['user_id']))
    myDB.view_all()
    return render_template("index.html", user_id=session['user_id'], online_users=myDB.get_all_logged_in_users())


def clear_session():
    session['logged_in'] = None
    session['facebook_token'] = None
    session['user'] = None
    session['user_id'] = None


@app.route("/")
def login():
    clear_session()
    return render_template("login.html")


@app.route("/logout")
def logout():
    myDB.user_logout(session['user_id'])
    clear_session()
    flash("You just logged out")
    return redirect(url_for('login'))


def str_to_bool(s):
    if 'true' in str(s):
        return True
    elif 'false' in str(s):
        return False
    else:
        raise ValueError


@app.route("/grant-<user_id>-<read>-<write>", methods=["POST", "GET"])
def grant_access(user_id, read, write):
    if int(session['user_id']) == 1139661149799278:
        print("granting" + user_id + "read: " + read + "write: " + write + "permissions")
        myDB.add_user_permission(user_id, read, write)
        auth_key = myDB.get_auth_key(user_id)
        PB.grant_access(auth_key, str_to_bool(read), str_to_bool(write))
    else:
        print("Who are you?")
        return json.dumps({"access": "denied"})
    return json.dumps({"access": "denied"})


@app.route("/get_auth_key", methods=["POST", "GET"])
def get_auth_key():
    print("Creating authkey for " + session['user'])
    auth_key = create_auth_key()
    myDB.add_auth_key(int(session['user_id']), auth_key)
    (read, write) = myDB.get_user_access(int(session['user_id']))

    PB.grant_access(auth_key, read, write)
    auth_response = {"authKey": auth_key, "cipherKey": PB.cipherKey}
    json_response = json.dumps(auth_response)
    return str(json_response)


def salt(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_auth_key():
    s = salt(10)
    hashing = hashlib.sha256((str(session['facebook_token']) + s).encode('utf-8'))
    return hashing.hexdigest()


@app.route("/keep_alive", methods=["GET"])
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(str(parsed_json))
    return str(parsed_json)


if __name__ == "__main__":
    app.run()
