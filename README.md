# Savings Bot

Django project for managing and handle all possible problems during product development in team

## Check it out!

[Savings Bot deployed to Render](https://savingbot.onrender.com)

It works slowly according to usage free database and hosting. 

### Admin User (for [link](https://savingbot.onrender.com/admin/))

* Username: Admin
* Password: 123admin123



## For local usage: Installation

Python3 and ngrok must be already installed

```shell
git clone https://github.com/kamilla-boiko/savings-bot
cd savings_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ngrok config add-authtoken <your_token>
ngrok http 8000  # need to parse Forwarding and set it to .env -> WEBHOOK_URL
python manage.py migrate
python manage.py runserver  # starts Django Server
```

## Features

* Add, show and delete savings for every user
* Show profile info

## Environment variables

This project uses environment variables to store sensitive or configurable data.
The variables are stored in a file named .env, which should be created in the
project's root directory.
Please follow the instructions below to set up the environment variables for your local development.

### .env file

Create a file named .env in the root directory of the project and add the following variables
with their corresponding values.

### .env_sample file

A file named .env_sample is included in the repository as a template for setting up the .env file.
It contains the names of the environment variables without their values.
You can use it as a reference when creating your own .env file.
