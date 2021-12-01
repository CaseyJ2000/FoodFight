"""Handles all requests to the yelp api"""
import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("CLIENT_ID")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
URL_ID = "https://api.yelp.com/v3/businesses/"


def get_restaurant(term, location):
    """Method to search for restaurants"""
    parameters = {"term": term, "location": location}

    response = requests.get(url=BASE_URL, params=parameters, headers=HEADERS)
    data = response.json()
    restaurant_ids = []
    name = []
    location = []
    image = []
    yelp_url = []
    category = []
    review_count = []
    rating = []
    transactions = []
    address = []

    for i in data["businesses"]:
        restaurant_ids.append(i["id"])
        name.append(i["name"])
        location.append(i["location"]["city"])
        image.append(i["image_url"])
        yelp_url.append(i["url"])
        category.append(i["categories"][0]["title"])
        review_count.append(i["review_count"])
        rating.append(i["rating"])
        transactions.append(i["transactions"])
        address.append(i["location"]["display_address"][1])

    return (
        name,
        image,
        location,
        restaurant_ids,
        yelp_url,
        category,
        review_count,
        rating,
        transactions,
        address,
    )


def get_restaurant_details(restaurant_dict, num_of_restaurants):
    """Returns infomation on the business ids in a dict passed to"""
    i = 0
    name = []
    image = []
    yelp_url = []
    rating = []
    length = min(len(restaurant_dict), num_of_restaurants)
    for key in restaurant_dict.keys():
        if i == num_of_restaurants:
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
