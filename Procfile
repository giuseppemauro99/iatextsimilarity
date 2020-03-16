#web: gunicorn gettingstarted.wsgi --log-level=debug
web: waitress-serve --port=$PORT gettingstarted.wsgi:application