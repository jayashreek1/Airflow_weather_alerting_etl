from airflow.decorators import task
import json
import sys

sys.path.append('/Users/jayashree/ETLWeather/dags')
from tasks.utils import OUTPUT_DIR, get_file_timestamp, logger

@task(task_id="save_weather_report", trigger_rule='all_success')
def save_weather_report(transformed_data):
    logger.info("Saving weather data to files")
    
    timestamp = get_file_timestamp()
    
    json_file_path = f"{OUTPUT_DIR}/weather_data_{timestamp}.json"
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=4)
        
    logger.info(f"Weather data saved to {json_file_path}")
    return json_file_path
