FROM python:latest

# RUN pip install ipython mariadb requests bs4

ADD requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /pg

COPY bookApp/ ./bookApp/
COPY scripts/ ./scripts/
COPY TestData/ ./TestData/

# ENTRYPOINT ["ipython3"]
ENTRYPOINT ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "bookApp.source.app:app"]
