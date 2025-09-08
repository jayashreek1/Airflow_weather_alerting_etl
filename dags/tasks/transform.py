"""
Task for transforming the raw weather data.
"""
from airflow.decorators import task
import sys
import os

# Add dags directory to path so we can import the utils module
sys.path.append('/Users/jayashree/ETLWeather/dags')
from tasks.utils import LATITUDE, LONGITUDE, get_timestamp, logger

@task(task_id="transform_weather_data")
def transform_weather_data(weather_data):
    """
    Transform the extracted weather data into a structured format.
    
    Args:
        weather_data (dict): Raw weather data from the API
        
    Returns:
        dict: Transformed weather data with selected fields
    """
    logger.info("Transforming raw weather data")
    
    current_weather = weather_data['current_weather']
    transformed_data = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'temperature': current_weather['temperature'],
        'windspeed': current_weather['windspeed'],
        'winddirection': current_weather['winddirection'],
        'weathercode': current_weather['weathercode'],
        'timestamp': get_timestamp()
    }
    
    logger.info(f"Transformed data: Temperature: {transformed_data['temperature']}°C, " 
                f"Weather Code: {transformed_data['weathercode']}")
    
    return transformed_data
