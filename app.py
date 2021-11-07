import os
from dotenv import load_dotenv, find_dotenv
import flask
from flask.helpers import flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_user,
    current_user,
    LoginManager,
    UserMixin,
    login_required,
)
from requests.api import request
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000), unique=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        return self.username


db.create_all()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


@app.route('/index')
@login_required
def index():
    return flask.render_template("index.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flask.flash("Username taken")
            return flask.redirect(flask.url_for('signup'))

        new_user = User(username=username,
                        password=generate_password_hash(password,
                                                        method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return flask.redirect(flask.url_for('login'))
    else:
        return flask.render_template("signup.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flask.flash("Username or password bad")
            return flask.redirect(flask.url_for('login'))
        login_user(user)
        return flask.redirect(flask.url_for('index'))
    else:
        return flask.render_template('login.html')


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    return flask.redirect(flask.url_for('login'))


if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "8081")),
            debug=True)
