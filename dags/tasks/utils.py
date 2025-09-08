"""
Utility functions and constants for the weather ETL pipeline.
"""
import os
import logging
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)

# Latitude and longitude for the desired location
LATITUDE = '13.0827'
LONGITUDE = '80.125'
API_CONN_ID = 'open_meteo_api'

# Email recipient (can be overridden by environment variable)
EMAIL_RECIPIENT = os.getenv('AIRFLOW_EMAIL_RECIPIENT', 'jayashree.kammu@gmail.com')

# Output directory for weather data
OUTPUT_DIR = '/opt/airflow/dags/output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Weather code mapping
WEATHER_CODES = {
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

def get_timestamp(format_str='%Y-%m-%d %H:%M:%S'):
    """Return current timestamp in specified format."""
    return datetime.now().strftime(format_str)

def get_file_timestamp():
    """Return timestamp format suitable for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
