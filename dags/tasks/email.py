from airflow.operators.email_operator import EmailOperator
from datetime import datetime
import sys

sys.path.append('/Users/jayashree/ETLWeather/dags')
from tasks.utils import EMAIL_RECIPIENT, logger

def create_email_task(html_content):
    try:
        email_task = EmailOperator(
            task_id='send_weather_email',
            to=EMAIL_RECIPIENT,
            subject=f'Weather Report - {datetime.now().strftime("%Y-%m-%d")}',
            html_content=html_content,
            trigger_rule='all_success'
        )
        logger.info(f"Email task created, will send report to {EMAIL_RECIPIENT}")
        return email_task
    except Exception as e:
        logger.error(f"Could not create email task: {str(e)}")
        return None
