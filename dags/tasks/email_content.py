from airflow.decorators import task
import sys

sys.path.append('/Users/jayashree/ETLWeather/dags')
from tasks.utils import WEATHER_CODES, logger

@task(task_id="prepare_email_content")
def prepare_email_content(transformed_data):
    logger.info("Preparing email content from transformed data")
    weather_description = WEATHER_CODES.get(transformed_data['weathercode'], "Unknown")
    email_content = f"""
    <h1>Weather Report</h1>
    <p><strong>Date:</strong> {transformed_data['timestamp']}</p>
    <p><strong>Location:</strong> Latitude {transformed_data['latitude']}, Longitude {transformed_data['longitude']}</p>
    <h2>Current Weather Conditions:</h2>
    <ul>
        <li><strong>Temperature:</strong> {transformed_data['temperature']}°C</li>
        <li><strong>Wind Speed:</strong> {transformed_data['windspeed']} km/h</li>
        <li><strong>Wind Direction:</strong> {transformed_data['winddirection']}°</li>
        <li><strong>Weather Condition:</strong> {weather_description}</li>
    </ul>
    <p>This report was generated automatically by Airflow.</p>
    """
    
    logger.info("Weather report prepared for email")
    return email_content
