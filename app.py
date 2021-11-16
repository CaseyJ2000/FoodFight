"""Loads the app"""
import os
from flask.templating import render_template
import requests
import operator
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_user,
    current_user,
    LoginManager,
    UserMixin,
    login_required,
)
import flask
from requests.api import request
from werkzeug.security import generate_password_hash, check_password_hash
import re
from yelp import getRestaurant, getRestaurantDetails


load_dotenv(find_dotenv())

app = flask.Flask(__name__)
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")
NUM_OF_PARTY_RECS = 5
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


class liked_biz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)


db.create_all()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    """loads user"""
    return User.query.get(user_name)


@app.route("/menu")
@login_required
def menu():
    """Loads menu webpage"""
    return flask.render_template("menu.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search_results():
    if flask.request.method == "POST":
        newterm = flask.request.form.get("term")
        newlocation = flask.request.form.get("location")

        try:
            restaurantInfo = getRestaurant(newterm, newlocation)
        except KeyError:
            errorMsg = ""

            if newterm == "" and newlocation == "":
                errorMsg = "term and location empty"
            elif newterm == "":
                errorMsg = "term empty"
            elif newlocation == "":
                errorMsg = "location empty"
            else:
                errorMsg = "no results found"

            return flask.render_template("error.html", errorMsg=errorMsg)

        name = restaurantInfo[0]
        image = restaurantInfo[1]
        location = restaurantInfo[2]
        biz_id = restaurantInfo[3]

        return flask.render_template(
            "search.html",
            search_query=True,
            location=location,
            image=image,
            name=name,
            biz_id=biz_id,
        )

    return flask.render_template("search.html")


@app.route("/like", methods=["POST"])
def like():

    business_id = flask.request.form.get("Like")
    if business_id == "":
        return flask.redirect(flask.request.referrer)
    username = current_user.username
    liked_restaurants = liked_biz.query.filter_by(
        username=username, business_id=business_id
    ).first()
    if not liked_restaurants:
        db.session.add(liked_biz(business_id=business_id, username=username))
        db.session.commit()
    return flask.redirect(flask.request.referrer)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Endpoint for signup"""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        repeatedPassword = flask.request.form.get("repeatedPassword")

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not (re.fullmatch(regex, username)):
            flask.flash("Incorrect email format")
            return flask.redirect(flask.url_for("signup"))

        if not (password == repeatedPassword):
            flask.flash("Passwords do not match")
            return flask.redirect(flask.url_for("signup"))
        user = User.query.filter_by(username=username).first()
        if user:
            flask.flash("Email already in use, please retry with a different email!")
            return flask.redirect(flask.url_for("signup"))

        new_user = User(
            username=username,
            password=generate_password_hash(password, method="sha256"),
        )

        db.session.add(new_user)
        db.session.commit()

        return flask.redirect(flask.url_for("login"))
    else:
        return flask.render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """Endpoint for login"""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flask.flash("Incorrect Username or Password. Try again!")
            return flask.redirect(flask.url_for("login"))

        login_user(user)
        return flask.redirect(flask.url_for("menu"))
    else:
        return flask.render_template("login.html")


@app.route("/")
def main():
    """Origin for user Login"""
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("menu"))
    return flask.redirect(flask.url_for("login"))


@app.route("/party", methods=["POST", "GET"])
def get_party_rec():

    if flask.request.method == "POST":
        people_in_party = flask.request.form.get("people_in_party")
        party_members = people_in_party.split(" ")
        restaurant_dict = {}
        for user in party_members:
            current_user = liked_biz.query.filter_by(username=user).all()
            if current_user == []:
                flask.flash(f"{user} could not be found")
            for row in current_user:
                if restaurant_dict.get(row.business_id) == None:
                    restaurant_dict.update({row.business_id: 1})
                else:
                    new_amount = restaurant_dict.get(row.business_id) + 1
                    restaurant_dict.update({row.business_id: new_amount})
        sorted_dict = dict(
            sorted(restaurant_dict.items(), key=operator.itemgetter(1), reverse=True)
        )

        restaurantDetails = getRestaurantDetails(sorted_dict, NUM_OF_PARTY_RECS)
        return flask.render_template(
            "party.html",
            recieved_party_data=True,
            name=restaurantDetails["name"],
            image=restaurantDetails["image"],
            yelp_url=restaurantDetails["yelp_url"],
            rating=restaurantDetails["rating"],
            length=restaurantDetails["length"],
        )
    else:
        return flask.render_template("party.html")


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8081")), debug=True
    )
