FROM python:3.9-slim

ENV NEW_RELIC_CONFIG_FILE=newrelic.ini

WORKDIR /rest_api

COPY . .

RUN pip install -r requirements.txt

CMD ["newrelic-admin", "run-program", "python", "app.py"]