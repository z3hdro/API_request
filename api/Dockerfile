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
RUN pip install -r requirements.txt

# copy entrypoint.sh
# COPY ./entrypoint.sh /opt/app/entrypoint.sh

# copy project
COPY . /opt/app

# run 
CMD [ "executable" ]