FROM python:latest

RUN pip install ipython mariadb requests bs4

ADD requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /pg

COPY *.py ./

ENTRYPOINT ["ipython3"]
