# File Manager

<!-- [![Build Status](https://travis-ci.com/ivcmartello/registrobrepp.svg?branch=master)](https://travis-ci.com/ivcmartello/file_manager.svg?token=YxevxaQeJibtDDNh8ij8&branch=main) -->

This project is for test and implement an application that can store files and create folders.

- The main page has a boxes to create folders and upload files.

## Some technologies approached

- Python >= 3.9

- Django >= 4.0

- Docker

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes (Mac OS or Linux).

### Prerequisites

What things you need to install if you don't have:

- ### [Python](https://github.com/pyenv/pyenv) >= 3.9

- ### [pip](https://pip.pypa.io/en/stable/installing/)

- ### Git

```
## On Ubuntu

> sudo apt-get update
> sudo apt-get install -y gcc libz-dev netcat sqlite3 libsqlite3-dev
```

- ### [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) - Optional

### Installing

Follow the instructions to get a development environment running:

The application will use sqlite3 as the default database.

Clone or download the repository.

```
> git clone https://github.com/ivcmartello/file_manager.git
```

Access the folder:

```
cd file_manager
```

## **All the commands need to be done on main project folder (The folder where you cloned or unzip the files).**

Create a file .env with your configurations (Ex.):

```
PYTHON=../venv/bin/python
VENV=../venv
BIN=../venv/bin
DEBUG=False

SECRET_KEY=YOUR SECRET KEY
ALLOWED_HOSTS=* 127.0.0.1 localhost
```

There is a Makefile with some shortcuts. To show the help menu type:

```
> make
```

```
help                 Show this help
venv                 Make a new virtual environment
install              Make venv and install requirements
migrate              Make and run migrations
super                Create super user to access admin system
test                 Run tests
run                  Run the Django server
start                Install requirements, apply migrations, then start development server
```

If you prefer keep following the instructions instead make commands feel free.

Create a virtual environment:

```
> python3 -m venv ../venv
```

Active the virtual environment:

```
> source ../venv/bin/activate
```

Install requirements:

```
> pip install -r requirements-dev.txt
```

Run migrations:

```
> python3 manage.py migrate
```

Create a super user (Optional):

```
> python3 manage.py createsuperuser
```

Run the application:

```
> python3 manage.py runserver
```

Access the address on your browser:

<http://localhost:8000>

<http://localhost:8000/api/>

## Running the tests

How to run the tests:

```
> DJANGO_SETTINGS_MODULE=file_manager.settings_test coverage erase && coverage run --source="file_manager_app" manage.py test --verbosity=2 --failfast && coverage report -m
```

## Running project on Docker

How to run the application on docker (use "--build" parameter just in the first time):

```
> docker-compose up -d --build
```

Create super user to access admin site (Optional):

```
> docker-compose exec web python manage.py createsuperuser
```

Access the address on your browser:

<http://localhost:8000>

<http://localhost:8000/api/>

Closing:

```
> docker-compose down
```