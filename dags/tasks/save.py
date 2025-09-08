"""
Task for saving weather data to files.
"""
from airflow.decorators import task
import json
import sys

# Add dags directory to path so we can import the utils module
sys.path.append('/Users/jayashree/ETLWeather/dags')
from tasks.utils import OUTPUT_DIR, get_file_timestamp, logger

@task(task_id="save_weather_report", trigger_rule='all_success')
def save_weather_report(transformed_data):
    """
    Save the weather report to files.
    
    Args:
        transformed_data (dict): Transformed weather data
        
    Returns:
        str: Path to the saved JSON file
    """
    logger.info("Saving weather data to files")
    
    timestamp = get_file_timestamp()
    
    # Save JSON data
    json_file_path = f"{OUTPUT_DIR}/weather_data_{timestamp}.json"
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=4)
        
    logger.info(f"Weather data saved to {json_file_path}")
    return json_file_path
