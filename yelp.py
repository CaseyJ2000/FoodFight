import os
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


def getRestaurant(term, location):
    PARAMETERS = {"term": term, "location": location}

    response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)

    data = response.json()
    id = []
    name = []
    location = []
    image = []
    rating = []
    category = []
    hours = []

    for i in data["businesses"]:
        id.append(i["id"])
        name.append(i["name"])
        location.append(i["location"]["city"])
        image.append(i["image_url"])
        rating.append(i["rating"])
        category.append(i["categories"])

    DATA = {
        "name": name,
        "location": location,
        "image": image,
        "rating": rating,
        "category": category,
    }

    datalist = []
    datalist.append(DATA)
    biz_id = id
    biz_name = name
    biz_image = image
    biz_location = location
    biz_rating = rating
    biz_category = category

    return (
        biz_name,
        biz_image,
        biz_location,
        biz_id,
        biz_rating,
        biz_category,
    )
