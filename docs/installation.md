### Correct installation of the package:


* ##### Create a virtual environment and activate it
```
cd hotel-api
python3 -m venv venv
source venv/bin/activate
```
* ##### Install Poetry to manage all dependencies
```
pip install poetry
```
##### (However, you can install it without pip if you want)
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
* ##### Install all dependencies
```
poetry install
```
* ##### Create a .env file
```
# Here's an example

POSTGRES_USER = "user"
POSTGRES_PASSWORD = "password"
POSTGRES_SERVER = "localhost"
POSTGRES_DATABASE = "database"
POSTGRES_TEST_DATABASE = "test-database"
ALGORITHM = "algorithm"
JWT_SECRET_KEY = "jwt_secret_key"
JWT_REFRESH_SECRET_KEY = "jwt_refresh_secret_key"
```
* ##### Create a working database with Alembic
```
alembic revision --autogenerate
alembic upgrade head
```
* ##### Run the app visually Swagger UI
```
uvicorn main:app --reload
```
