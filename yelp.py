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

    if not data.get("businesses"):
        raise ValueError("no results found")
    elif term == "" and location == "":
        raise ValueError("term and location empty")
    elif term == "":
        raise ValueError("term empty")
    elif location == "":
        raise ValueError("location empty")
    if type(location) == str and type(term) == str:
        id = []
        name = []
        location = []
        image = []
        datalist = []
        for i in data["businesses"]:
            id.append(i["id"])
            name.append(i["name"])
            location.append(i["location"]["city"])
            image.append(i["image_url"])

        # DATA = {"id": id, "name": name, "location": location, "image": image}
        # datalist = []
        # datalist.append(DATA)
        # biz_id = id
        # biz_name = name
        # biz_image = image
        # biz_location = location
    return (name, image, location, id)
