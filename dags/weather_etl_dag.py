"""
Main DAG definition for the Weather ETL Pipeline.

This DAG:
1. Extracts weather data from the Open-Meteo API
2. Transforms the data into a more usable format
3. Prepares email content with a weather report
4. Saves the weather data to a JSON file
5. Sends an email with the weather report (if SMTP is configured)
"""

from airflow import DAG
from airflow.utils.dates import days_ago
import os
import sys

# Add the current directory to sys.path so Python can find our task modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tasks.utils import EMAIL_RECIPIENT
from tasks.extract import extract_weather_data
from tasks.transform import transform_weather_data
from tasks.email_content import prepare_email_content
from tasks.save import save_weather_report
from tasks.email import create_email_task

# Define default arguments
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "email": [EMAIL_RECIPIENT],
    "email_on_failure": True,
}

# Create the DAG
with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",  # Run every hour (at minute 0)
    catchup=False,
    tags=["weather", "etl", "api"],
) as dag:

    # Define task instances
    extract_task = extract_weather_data()
    # transform_task = transform_weather_data(extract_task)
    # content_task = prepare_email_content(transform_task)
    # save_task = save_weather_report(transform_task)

    # Create email task (may be None if SMTP not configured)
    # email_task = create_email_task(content_task)

    # Set task dependencies
    # extract_task >> transform_task >> save_task


    # Add email task if it was created successfully
    # if email_task:
    #     content_task >> email_task