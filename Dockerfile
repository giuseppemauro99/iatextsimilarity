FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /gettingstarted
WORKDIR /hello
COPY . /gettingstarted/
RUN pip install -r requirements.txt