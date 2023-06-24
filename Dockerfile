FROM python:3.9-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app app

CMD [ "python", "app" ]