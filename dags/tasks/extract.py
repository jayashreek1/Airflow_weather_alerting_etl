"""
Task for extracting weather data from the Open-Meteo API.
"""
from airflow.decorators import task
from airflow.providers.http.hooks.http import HttpHook
from .utils import LATITUDE, LONGITUDE, API_CONN_ID, logger

@task(task_id="extract_weather_data")
def extract_weather_data():
    """
    Extract weather data from Open-Meteo API using Airflow Connection.
    
    Returns:
        dict: The JSON response from the API containing weather data
    """
    logger.info(f"Extracting weather data for latitude={LATITUDE}, longitude={LONGITUDE}")
    
    # Use HTTP Hook to get connection details from Airflow connection
    http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

    # Build the API endpoint
    endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true&timezone=Asia/Kolkata'

    # Make the request via the HTTP Hook
    response = http_hook.run(endpoint)

    if response.status_code == 200:
        logger.info("Successfully retrieved weather data from API")
        return response.json()
    else:
        error_msg = f"Failed to fetch weather data: {response.status_code}"
        logger.error(error_msg)
        raise ValueError(error_msg)
