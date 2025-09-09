"""
Task for extracting weather data from the Open-Meteo API.
"""
from airflow.decorators import task
from airflow.providers.http.hooks.http import HttpHook
from .utils import LATITUDE, LONGITUDE, API_CONN_ID, logger

@task(task_id="extract_weather_data")
def extract_weather_data():
    logger.info(f"Extracting weather data for latitude={LATITUDE}, longitude={LONGITUDE}")
    http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
    endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true&timezone=Asia/Kolkata'
    response = http_hook.run(endpoint)
		
    if response.status_code == 200:
        logger.info("Successfully retrieved weather data from API")
        return response.json()
    else:
        error_msg = f"Failed to fetch weather data: {response.status_code}"
        logger.error(error_msg)
        raise ValueError(error_msg)
