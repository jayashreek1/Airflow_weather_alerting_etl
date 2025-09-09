import os
import sys

from airflow import DAG
from airflow.utils.dates import days_ago

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tasks.utils import EMAIL_RECIPIENT
from tasks.extract import extract_weather_data
from tasks.transform import transform_weather_data
from tasks.email_content import prepare_email_content
from tasks.save import save_weather_report
from tasks.email import create_email_task

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "email": [EMAIL_RECIPIENT],
    "email_on_failure": True,
}


with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False, # Historical data backfills.	
    tags=["weather", "etl", "api"],
) as dag:

    extract_task = extract_weather_data()
    transform_task = transform_weather_data(extract_task)
    save_task = save_weather_report(transform_task)
    content_task = prepare_email_content(transform_task)
    email_task = create_email_task(content_task)
    

    extract_task >> transform_task >> save_task >> content_task >> email_task
