# HotelScape

## Overview
HotelScape is created for hotel administrators and receptionists who want to effectively manage the typical hotel workflow.<br/>
Full documentation is available here: https://tyaroshko.github.io/hotel-api/

## Software Requirements
* Python3
* PostgreSQL and GUI tool for viewing the databases<br/>(pgAdmin4, OmniDB, DBeaver or any other of your choice)
* Browser (preferably Google Chrome)
* IDE (preferably VS Code or JetBrains PyCharm) or text editor to play around with the code

## Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
## Install Poetry and necessary dependencies
```
pip install poetry
poetry install
```
## Connect PostgreSQL via .env file
Create a .env file with all your environment variables. <br/>
It should look like this:
```
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "password"
POSTGRES_SERVER = "localhost"
POSTGRES_DATABASE = "database"
POSTGRES_TEST_DATABASE = "test-database"
ALGORITHM = "algorithm"
JWT_SECRET_KEY = "jwt_secret_key"
JWT_REFRESH_SECRET_KEY = "jwt_refresh_secret_key"
```
## Create migrations via Alembic
```
alembic revision --autogenerate     # To create a new revision
alembic upgrade head                # To upgrade your db
alembic downgrade head              # You can always downgrade in case something goes wrong
```
## Test the API via Swagger UI
Run the API using Uvicorn:
```
uvicorn main:app --reload
```
and head to http://127.0.0.1:8000/docs
