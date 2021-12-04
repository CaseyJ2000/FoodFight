<h1 align="center">FoodFight</h1>

###  [Link to Heroku](https://food-fight-gsu-sprint2.herokuapp.com/)

# Table of contents

- [App Description](#App-Description)
- [Installation Requirements](#Installation-Requirements)
- [Local Setup](#Local-Setup)
- [Features](#Features)
- [Linting](#Linting)
- [Technologies](#Techologies)
- [Contributors](#Contributors)


##  App Description 
This is a web app that is hosted on heroku that is built with the flask framework and styled with css/bootstrap. It uses yelp api and allows the user to search up a specific type of restaurant or food with a location, the user is then able to like any of the restaurants displayed.  The user is also able to create a party and add other user’s emails so that you are able to find out the most liked restaurants between you and your party members.

# Installation Requirements
Install the following by typing the commands in terminal

### Install flask

```pip install flask```

### Install requests package

```pip install requests```

### Install dotenv package

```pip install python-dotenv```

### Install Flask-login

```pip install flask-login```

### Install psycopg2 - This will allow you to interact with local DBs

 ```pip install psycopg2-binary```

### Install Flask-SQLAlchemy

```pip install Flask-SQLAlchemy==2.1```

# Local Setup

1. Create a `.env` file in the top-level directory and enter the following as its contents:
```
DATABASE_URL = '<insert postgresql database link>’
SECRET_KEY = ‘<insert any string for secret key>’
export API_KEY = "<insert yelp api key>"
export CLIENT_ID = "<insert client id>"
```


2. run `python3 app.py` 

# Features
### Search 
You are able to search for a restaurant by name or by cuisine and supplying it with a location will yield results.

### Like a Restaurant
You are able to like restaurants after searching for your desired restaurant or cuisine of food!

### Create a Party
You are able to create a party with other registered user's emails seperated by a space to display you and your party's liked restuarants. The Restaurants displayed are sorted in a way that the restaurants with multiple likes across party memebers will be displayed at the top.

### Unlike a restaurant
You are able to remove a restaurant off of your profile by clicking the unlike button next to the restaurants in your profile page.

### Delete an account
You are able to delete an account by entering in the desired email that you want to remove.

### Profile Page
This displays the current logged in user's liked restaurants and allows you to unlike/remove any restaurants.

# Linting
The no-member error is being ignored in pylint. This is the case because the code will still continue to run and pylint is having a false postive.

# Technologies 
- Flask Framework
- HTML
- CSS/Bootstrap for styling
- Yelp API to get restaurant details such as location, ratings, and yelp url
- PostgreSQL to store User's emails and yelp business IDs


# Contributors 
[Casey Jobe](https://github.com/CaseyJ2000)

[Owen Bochner](https://github.com/owenbochner)

[Stephanie Olele](https://github.com/steph-o21)

[Sydney Yim](https://github.com/syim12)

[Victor Lam](https://github.com/Vikcho)

