from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.decorators import task
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import logging
import json
import os

# Set up logger
logger = logging.getLogger(__name__)

# Latitude and longitude for the desired location (London in this case)
LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
API_CONN_ID='open_meteo_api'

# Email recipient
EMAIL_RECIPIENT = 'jayashree.kammu@gmail.com'  # Change this to your email

# Output directory for weather data
OUTPUT_DIR = '/opt/airflow/dags/output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

default_args={
    'owner':'airflow',
    'start_date':days_ago(1),
    'email': [EMAIL_RECIPIENT],
    'email_on_failure': True
}

## DAG
with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dags:
    
    @task()
    def extract_weather_data():
        """Extract weather data from Open-Meteo API using Airflow Connection."""

        # Use HTTP Hook to get connection details from Airflow connection
        http_hook=HttpHook(http_conn_id=API_CONN_ID,method='GET')

        ## Build the API endpoint
        ## https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true
        endpoint=f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'

        ## Make the request via the HTTP Hook
        response=http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to fetch weather data: {response.status_code}")
        
    @task()
    def transform_weather_data(weather_data):
        """Transform the extracted weather data."""
        current_weather = weather_data['current_weather']
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return transformed_data
    
    @task()
    def prepare_email_content(transformed_data):
        """Format weather data for email."""
        # Convert weather code to description
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        weather_description = weather_codes.get(transformed_data['weathercode'], "Unknown")
        
        # Create email content
        email_content = f"""
        <h1>Weather Report</h1>
        <p><strong>Date:</strong> {transformed_data['timestamp']}</p>
        <p><strong>Location:</strong> Latitude {transformed_data['latitude']}, Longitude {transformed_data['longitude']}</p>
        <h2>Current Weather Conditions:</h2>
        <ul>
            <li><strong>Temperature:</strong> {transformed_data['temperature']}°C</li>
            <li><strong>Wind Speed:</strong> {transformed_data['windspeed']} km/h</li>
            <li><strong>Wind Direction:</strong> {transformed_data['winddirection']}°</li>
            <li><strong>Weather Condition:</strong> {weather_description} (Code: {transformed_data['weathercode']})</li>
        </ul>
        <p>This report was generated automatically by Airflow.</p>
        """
        
        # Also log the data
        logger.info("Weather report prepared for email")
        
        return email_content

    # Define tasks
    extract_task = extract_weather_data()
    transform_task = transform_weather_data(extract_task)
    content_task = prepare_email_content(transform_task)
    
    # 1. Save weather report to files
    @task(trigger_rule='all_success')
    def save_weather_report(html_content, transformed_data):
        """Save the weather report to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save HTML report
        html_file_path = f"{OUTPUT_DIR}/weather_report_{timestamp}.html"
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save JSON data
        json_file_path = f"{OUTPUT_DIR}/weather_data_{timestamp}.json"
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, indent=4)
            
        logger.info("Weather report saved to %s", html_file_path)
        logger.info("Weather data saved to %s", json_file_path)
        return html_file_path, json_file_path
    
    # 2. Send weather report via email (will fail if SMTP not configured properly)
    try:
        # Send email with weather data
        email_task = EmailOperator(
            task_id='send_weather_email',
            to=EMAIL_RECIPIENT,
            subject=f'Weather Report - {datetime.now().strftime("%Y-%m-%d")}',
            html_content=content_task,
            trigger_rule='all_success'
        )
    except Exception as e:
        # Log error but continue with file saving
        logger.error("Could not create email task: %s", str(e))
        email_task = None
    
    # Save the report to files (this will always run)
    save_task = save_weather_report(content_task, transform_task)
    
    # Set task dependencies
    extract_task >> transform_task >> content_task >> save_task
    
    # Add email task if it was created successfully
    if email_task:
        content_task >> email_task