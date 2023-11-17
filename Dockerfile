

FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN mkdir /librarymanagement


WORKDIR /librarymanagement


ADD . /librarymanagement/

# COPY spinup.sh /app/spinup.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT