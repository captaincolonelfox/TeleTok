FROM python:3.11.8-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app app

CMD [ "python", "app" ]