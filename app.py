import os
from dotenv import load_dotenv, find_dotenv
import flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_user,
    current_user,
    LoginManager,
    UserMixin,
    login_required,
)

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        return self.username


db.create_all()