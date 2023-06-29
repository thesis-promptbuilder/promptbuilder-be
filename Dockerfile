FROM python:3.10.12-slim

RUN apt-get -y update && apt-get install -y libzbar-dev

WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt

CMD python run.py