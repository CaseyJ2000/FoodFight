import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("CLIENT_ID")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": "Bearer %s" % API_KEY}

# define search parameters (practice with api)
PARAMETERS = {
    "term": "",
    "limit": 10,
    "offset": 50,
    "radius": 10000,
    "location": "Springfield, MA",
}

response = requests.get(url=BASE_URL, params=PARAMETERS, headers=HEADERS)

# Conver the JSON String
data = response.json()

# print the response
# print(data)
# print(data["businesses"])

# for item in data["businesses"]:
#     print(item["name"])

for i in range(10):
    try:
        biz = data["businesses"][i]["name"]
        print(biz)

    except KeyError:
        print("Couldn't fetch")
        break

# create exception for small cities so app doesn't break

# def getRestaurant():  # function for getting name of Restuarant
#     return
