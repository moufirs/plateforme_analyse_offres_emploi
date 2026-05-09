from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'firdaous',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='job_data_pipeline',
    default_args=default_args,
    description='Pipeline Scraping Jobs',
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # 🕷️ Scraping → envoie vers Kafka
   scrape = BashOperator(
    task_id='scrape_jobs',
    bash_command='cd /opt/airflow/project/job_scraper && scrapy crawl jobs'
)

wait = BashOperator(
    task_id='wait_kafka',
    bash_command='sleep 10'
)

silver = BashOperator(
    task_id='silver_layer',
    bash_command='cd /opt/airflow/project && python silver.py'
)

gold = BashOperator(
    task_id='gold_layer',
    bash_command='cd /opt/airflow/project && python gold.py'
)

load_dw = BashOperator(
    task_id='load_datawarehouse',
    bash_command='cd /opt/airflow/project && python load_dw.py'
)
scrape >> wait >> silver >> gold >> load_dw