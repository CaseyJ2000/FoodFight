import os
from flask.wrappers import Response
import requests
import json
import flask
from dotenv import load_dotenv, find_dotenv
from requests.api import get, request


load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("CLIENT_ID")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": "Bearer %s" % API_KEY}
URL_ID = "https://api.yelp.com/v3/businesses/"


def getRestaurant(term, location):
    PARAMETERS = {"term": term, "location": location}

    response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)
    data = response.json()
    id = []
    name = []
    location = []
    image = []
    for i in data["businesses"]:
        id.append(i["id"])
        name.append(i["name"])
        location.append(i["location"]["city"])
        image.append(i["image_url"])

    return (name, image, location, id)


def getRestaurantDetails(restaurant_dict, numOfRestaurants):
    i = 0
    name = []
    image = []
    yelp_url = []
    rating = []
    length = len(restaurant_dict)
    if length > numOfRestaurants:
        length = numOfRestaurants
    for key in restaurant_dict.keys():
        if i == numOfRestaurants:
            break
        response = requests.get(url=URL_ID + key, headers=HEADERS)
        data = response.json()
        name.append(data["name"])
        image.append(data["image_url"])
        yelp_url.append(data["url"])
        rating.append(data["rating"])

    return {
        "name": name,
        "image": image,
        "yelp_url": yelp_url,
        "rating": rating,
        "length": length,
    }
