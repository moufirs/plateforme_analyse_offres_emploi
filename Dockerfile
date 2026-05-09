FROM apache/airflow:2.7.0

USER airflow

RUN pip install --user scrapy kafka-python
