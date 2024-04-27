FROM python:3.9-slim

WORKDIR /movies

COPY . .

RUN pip install -r requirements.txt

COPY . .

CMD python app.py