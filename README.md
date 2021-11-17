<h1 align="center">FoodFight</h1>

###  [Link to Heroku](https://food-fight-gsu.herokuapp.com/)

# Table of contents

- [App Description](#App-Description)
- [Installation Requirements](#Installation-Requirements)
- [Local Setup](#Local-Setup)
- [Known Issues](#Known-Issues)
- [Linting](#Linting)


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

## Known Issues
After clicking the like button for a restaurant, you are redirected to the search page where you would need to search for restaurants again instead of it keeping you on the same page that shows all the restaurants with their corresponding like button.

# Linting
The no-member error is being ignored in pylint. This is the case because the code will still continue to run and pylint is having a false postive.

README is still a work in progress
