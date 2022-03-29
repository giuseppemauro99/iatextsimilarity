# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN echo $(pip --version)
RUN echo $(python --version)
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . /code/