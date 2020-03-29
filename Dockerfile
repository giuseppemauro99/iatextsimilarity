FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /gettingstarted
WORKDIR /gettingstarted
COPY . /gettingstarted/
RUN pip install -r requirements.txt