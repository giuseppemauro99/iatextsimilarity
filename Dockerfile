FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /gettingstarted
WORKDIR /gettingstarted
COPY . /gettingstarted/
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "-w", "4", "--bind_ip_all", "0.0.0.0:8000", "wsgi"]