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
    location_state = []

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
        location_state.append(i["location"]["state"])

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
        location_state,
    )


def get_restaurant_details(restaurant_dict, num_of_restaurants):
    """Returns infomation on the business ids in a dict passed to"""
    i = 0
    name = []
    image = []
    biz_id = []
    yelp_url = []
    rating = []
    category = []
    review_count = []
    location_city = []
    location_state = []
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
        biz_id.append(data["id"])
        category.append(data["categories"][0]["title"])
        review_count.append(data["review_count"])
        location_city.append(data["location"]["city"])
        location_state.append(data["location"]["state"])
    return {
        "name": name,
        "image": image,
        "yelp_url": yelp_url,
        "rating": rating,
        "length": length,
        "category": category,
        "biz_id": biz_id,
        "review_count": review_count,
        "location_city": location_city,
        "location_state": location_state,
    }
