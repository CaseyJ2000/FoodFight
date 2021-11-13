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

# define search parameters (practice with api)
# PARAMETERS = {
#     "term": "",
#     "limit": 10,
#     # "offset": 50,
#     # "radius": 10000,
#     "location": "Atlanta",
# }

# response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)

# # Convert the JSON String
# data = response.json()
# # print(data)
# for i in range(10):
#     try:
#         biz = data["businesses"][i]["name"]
#         print(biz)

#     except KeyError:
#         print("Couldn't fetch")
#         break
# # print the response
# print(data)
# print(data["businesses"])

# for item in data["businesses"]:
#     print(item["name"], item["image_url"], item["location"]["city"])


# create exception for small cities so app doesn't break


# def getRestaurant():  # function for getting name of Restuarant
#     PARAMETERS = {
#         "limit": 10,
#         "term": "seafood",
#         "location": "Chicago",
#     }

#     response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)

#     # response = requests.get(
#     #     f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}",
#     #     # params={"limit": 10},
#     #     headers=HEADERS,
#     # )
#     # Convert the JSON String
#     data = response.json()
#     # print(data)
#     for i in range(0, 10):
#         try:
#             biz = data["businesses"][i]["name"]
#             print(biz)
#         except KeyError:
#             print("Couldn't fetch")
#             break
#     # for i in range(0, 20):
#     biz_name = data["businesses"][i]["name"]
#     biz_image = data["businesses"][i]["image_url"]
#     biz_location = data["businesses"][i]["location"]["city"]

#     # print(biz_name, biz_image, biz_location)

#     return (biz_name, biz_image, biz_location)


# print(getRestaurant())

# PARAMETERS = {
#     "limit": 20,
#     "term": "seafood",
#     "location": "Chicago",
# }


# def main_request():
#     response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)
#     return response.json()


# def response(r):
#     return r["businesses"]["name"]


def getRestaurant():
    term = "cheesecake"
    location = "LA"
    PARAMETERS = {
        "limit": 20,
        "term": term,
        "location": location,
    }

    response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)

    data = response.json()
    name = []
    location = []
    image = []

    for i in data["businesses"]:
        name.append(i["name"])
        location.append(i["location"]["city"])
        image.append(i["image_url"])

    DATA = {"name": name, "location": location, "image": image}
    datalist = []
    datalist.append(DATA)
    biz_name = name
    biz_image = image
    biz_location = location
    return (biz_name, biz_image, biz_location)


# print(getRestaurant())
