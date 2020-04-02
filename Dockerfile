FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /gettingstarted
WORKDIR /gettingstarted
COPY . /gettingstarted/
RUN pip install -r requirements.txt

RUN mongo django_mongodb /gettingstarted/init-db/init-db.js

CMD [ "gunicorn", "-w", "4", "--bind_ip_all", "0.0.0.0:8000", "wsgi"]