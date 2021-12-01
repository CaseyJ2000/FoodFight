# pylint: disable=no-member
"""Loads the app"""
import re
import os
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
from werkzeug.security import generate_password_hash, check_password_hash
from yelp import get_restaurant, get_restaurant_details

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


class LikedBiz(db.Model):
    """Creates model for LikeBiz"""

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<User {self.username}> <business_id {self.business_id}>"

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


@app.route("/about")
@login_required
def about():
    """Loads about page"""
    return flask.render_template("about.html")


@app.route("/like", methods=["POST"])
def like():
    """Adds users liked restaurant to the database"""
    business_id = flask.request.form.get("Like")
    if business_id == "":
        return flask.redirect(flask.request.referrer)
    username = current_user.username
    liked_restaurants = LikedBiz.query.filter_by(
        username=username, business_id=business_id
    ).first()
    if not liked_restaurants:
        db.session.add(LikedBiz(business_id=business_id, username=username))
        db.session.commit()
    return flask.redirect(flask.url_for("profile"))
    # return flask.redirect(flask.request.referrer)


@app.route("/login", methods=["POST", "GET"])
def login():
    """Endpoint for login"""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        username = username.lower()
        password = flask.request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flask.flash("Incorrect Username or Password. Try again!")
            return flask.redirect(flask.url_for("login"))

        login_user(user)
        return flask.redirect(flask.url_for("menu"))

    return flask.render_template("login.html")


@app.route("/menu")
@login_required
def menu():
    """Loads menu webpage"""
    return flask.render_template("menu.html")


@app.route("/party", methods=["POST", "GET"])
@login_required
def get_party_rec():
    """End point for the party recommendations. Runs logic to recommend a list of restaurants"""
    if flask.request.method == "POST":
        people_in_party = flask.request.form.get("people_in_party")
        party_members = people_in_party.split(" ")
        restaurant_dict = {}
        for user in party_members:
            current_party_member = LikedBiz.query.filter_by(username=user).all()
            if current_party_member == []:
                flask.flash(f"{user} could not be found")
            for row in current_party_member:
                if restaurant_dict.get(row.business_id) is None:
                    restaurant_dict.update({row.business_id: 1})
                else:
                    new_amount = restaurant_dict.get(row.business_id) + 1
                    restaurant_dict.update({row.business_id: new_amount})
        sorted_dict = dict(
            sorted(restaurant_dict.items(), key=operator.itemgetter(1), reverse=True)
        )

        restaurant_details = get_restaurant_details(sorted_dict, NUM_OF_PARTY_RECS)
        return flask.render_template(
            "party.html",
            recieved_party_data=True,
            name=restaurant_details["name"],
            image=restaurant_details["image"],
            yelp_url=restaurant_details["yelp_url"],
            rating=restaurant_details["rating"],
            length=restaurant_details["length"],
        )

    return flask.render_template("party.html")


@app.route("/profile")
@login_required
def profile():
    username = current_user.username
    """Loads profile webpage"""
    return flask.render_template("profile.html", username=username)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search_results():
    """Endpoint for the search route"""
    if flask.request.method == "POST":
        newterm = flask.request.form.get("term")
        newlocation = flask.request.form.get("location")

        try:
            restaurant_info = get_restaurant(newterm, newlocation)
        except KeyError:
            error_msg = ""

            if newterm == "" and newlocation == "":
                error_msg = "term and location empty"
            elif newterm == "":
                error_msg = "term empty"
            elif newlocation == "":
                error_msg = "location empty"
            else:
                error_msg = "no results found"

            return flask.render_template("error.html", error_msg=error_msg)

        name = restaurant_info[0]
        image = restaurant_info[1]
        location = restaurant_info[2]
        biz_id = restaurant_info[3]
        yelp_url = restaurant_info[4]

        return flask.render_template(
            "search.html",
            search_query=True,
            location=location,
            image=image,
            name=name,
            biz_id=biz_id,
            yelp_url=yelp_url,
        )

    return flask.render_template("search.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Endpoint for signup"""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        username = username.lower()
        password = flask.request.form.get("password")
        repeated_password = flask.request.form.get("repeatedPassword")

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, username):
            flask.flash("Incorrect email format")
            return flask.redirect(flask.url_for("signup"))

        if not password == repeated_password:
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

    return flask.render_template("signup.html")


@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete_account():
    """Endpoint to delete account"""
    if flask.request.method == "POST":
        user_to_be_deleted = current_user.get_username()
        entered_username = flask.request.form.get("username")
        entered_username = entered_username.lower()
        if user_to_be_deleted == entered_username:
            LikedBiz.query.filter_by(username=user_to_be_deleted).delete()
            User.query.filter_by(username=user_to_be_deleted).delete()
            db.session.commit()

            flask.flash("Your account has been successfully deleted.")
            return flask.redirect(flask.url_for("login"))
        flask.flash("Email is incorrect")
    return flask.render_template("delete-account.html")


@app.route("/")
def main():
    """Origin for user Login"""
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("menu"))
    return flask.redirect(flask.url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8081")), debug=True
    )
