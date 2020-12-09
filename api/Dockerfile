# pull official base image
FROM python:3.8.3

# set work directory
WORKDIR /opt/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /opt/app/requirements.txt
RUN python3 -m pip install -r requirements.txt --no-cache-dir
# RUN \
#  apk add --no-cache postgresql-libs && \
#  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
#  python3 -m pip install -r requirements.txt --no-cache-dir && \
#  apk --purge del .build-deps

# copy entrypoint.sh
# COPY ./entrypoint.sh /opt/app/entrypoint.sh

# copy project
COPY . /opt/app

# run 
RUN [ "celery","-A","api","worker" ]