# Description:

This is an app created specifically for the Sentral's Developer Challenge Exercise – Activity Management.

The main objective of the challenge is to enhance the SimpleSIS application with an Activities section that allows a user to create/manage an activity/event.

# How to install:

1. Install Python 3.8
   1. Install `pipenv` using `pip install pipenv`
2. Install MySQL/MariaDB
   1. Create a new database
3. Clone the repository
4. Navigate to the project root folder and run `pipenv install` or `pipenv install --dev` to include dev dependencies
5. Modify the included `.env` file in the project folder with the details of the database you created
```
# Debug mode
DEBUG_MODE=True|1|False|0

# Secret key
SECRET_KEY=a default key is provided

# Database access
DATABASE_NAME=name of the database
DATABASE_HOST=database access domain or IP
DATABASE_PORT=database access port
DATABASE_USER=database user
DATABASE_PASS=database password
```
6. From the root folder of the project `pipenv run mg` to apply database migrations
7. Then, run `pipenv run load fixtures/fixtures.json` to load mock data

# How to run:

From the root folder of the project run `pipenv run start`

# How to log the app:

1. Head to `http://127.0.0.1:8000/login`
2. Use `john.doe@email.com || 12345` as login credentials

# How to log in as a super user (to add more mock data)

1. Head to `http://127.0.0.1:8000/admin/login`
2. Use `maccorone@gmail.com || 12345` as login credentials

# Extra info:

Additional shortcuts for Django manage commands can be found in the `Pipfile`