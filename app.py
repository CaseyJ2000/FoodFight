"""Loads the app"""
import os
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import (login_user, current_user, LoginManager, UserMixin,
                         login_required)
import flask
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """Creates model for User. Username is the identifier"""
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000), unique=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        """Returns username"""
        return self.username


db.create_all()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    """loads user"""
    return User.query.get(user_name)


@app.route('/menu')
@login_required
def menu():
    """Loads menu webpage"""
    return flask.render_template('menu.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """Endpoint for signup"""
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
        return flask.render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Endpoint for login"""
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flask.flash("Username or password bad")
            return flask.redirect(flask.url_for('login'))
        login_user(user)
        return flask.redirect(flask.url_for('menu'))
    else:
        return flask.render_template('login.html')


@app.route('/')
def main():
    """Origin for user Login"""
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('menu'))
    return flask.redirect(flask.url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
