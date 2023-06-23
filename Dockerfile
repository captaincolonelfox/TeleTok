FROM python:3.9-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app ./

CMD [ "python", "app" ]