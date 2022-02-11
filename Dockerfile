# pull official base image
FROM python:3

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install os dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libz-dev \
    netcat \
    sqlite3 \
    libsqlite3-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY file_manager/ /usr/src/app/file_manager/
COPY file_manager_app/ /usr/src/app/file_manager_app/
COPY ./.env .
COPY ./docker-entrypoint.sh .
COPY ./manage.py .

RUN chmod +x *.sh
