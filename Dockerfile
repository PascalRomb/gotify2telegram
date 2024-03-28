FROM python:3.9.6-alpine

WORKDIR /app

#COPY  src/ app
COPY requirements.txt /app/requirements.txt 
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN apk add --update alpine-sdk

RUN pip install -r requirements.txt

CMD [ "python", "/app/main.py" ]
