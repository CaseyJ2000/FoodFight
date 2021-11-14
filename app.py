"""Loads the app"""
import os
from dotenv import load_dotenv, find_dotenv
from yelp import getRestaurant
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

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

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


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Endpoint for signup"""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            flask.flash("Username taken")
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


@app.route("/like", methods=["POST"])
def like():
    business_id = flask.request.form.get("Like")

    # try:
    #     access_token = getRestaurant()
    #     get(business_id, access_token)
    # except Exception:
    #     flask.flash("Invalid artist ID entered")
    #     return flask.redirect(flask.url_for("index"))

    username = current_user.username
    db.session.add(liked_biz(business_id=business_id, username=username))
    db.session.commit()
    return flask.redirect(flask.url_for("search"))


@app.route("/search")
@login_required
def search():
    term = "Cheesecake"
    location = "NYC"
    restaurantInfo = getRestaurant(term, location)
    name = restaurantInfo[0]  # biz name
    image = restaurantInfo[1]  # biz image
    location = restaurantInfo[2]  # biz location
    length = len(name)

    """Loads search webpage"""
    return flask.render_template(
        "search.html", image=image, location=location, name=name, length=length
    )


@app.route("/search_results", methods=["GET", "POST"])
@login_required
def search_results():
    term = "Cheesecake"
    location = "NYC"
    if flask.request.method == "POST":
        # store as global variable or pass to method
        newterm = flask.request.form.get("term")
        newlocation = flask.request.form.get("location")

        restaurantInfo = getRestaurant(newterm, newlocation)
        name = restaurantInfo[0]  # biz name
        image = restaurantInfo[1]  # biz image
        location = restaurantInfo[2]  # biz location

        return flask.render_template(
            "search.html",
            term=term,
            location=location,
            image=image,
            name=name,
        )


@app.route("/login", methods=["POST", "GET"])
def login():
    """Endpoint for login"""
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flask.flash("Username or password bad")
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


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8081")), debug=True
    )
