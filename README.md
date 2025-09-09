# ETL Weather App

## Overview

ETL Weather App is a data pipeline that extracts weather data from the Open-Meteo API, transforms it into a useful format, and loads it by both saving to files and optionally sending email reports. The pipeline is built using Apache Airflow and runs on Docker containers.

## Features

- **Extract**: Fetches real-time weather data from the Open-Meteo API for any location
- **Transform**: Processes raw weather data into a meaningful format with human-readable weather descriptions
- **Load**: Dual output methods:
  - Saves weather reports as HTML files
  - Saves weather data as JSON files
  - Sends email reports (when properly configured)
- **Scheduling**: Runs on a configurable schedule (daily by default)
- **Containerized**: Fully Dockerized for easy deployment

## Project Structure

```
etl_weather/
├── dags/                    # Airflow DAG files
│   ├── etl_weather.py       # Main ETL pipeline DAG
│   └── output/              # Directory where weather reports are saved
		└── tasks/ 							 # Set of tasks
├── docker-compose.yaml      # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── requirements.txt         # Python dependencies
├── setup.sh                 # Setup script for easy installation
└── README.md                # This documentation
```

## Prerequisites

- Docker and Docker Compose
- Internet connection (to access the Open-Meteo API)
- (Optional) SMTP access for sending emails

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/jayashreek1/Airflow_weather_alerting_etl.git
   cd etl_weather
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually start the containers:
   ```bash
   docker-compose -f docker-compose.yaml up -d
   ```

3. Access the Airflow web interface:
   - URL: http://localhost:8082
   - Username: admin
   - Password: admin

## Configuration

### Weather Location

You can change the location for which weather data is fetched by modifying the latitude and longitude variables in `dags/etl_weather.py`:

```python
# Latitude and longitude for the desired location (London by default)
LATITUDE = '13.0827'
LONGITUDE = '0.80.125'
```

### Email Configuration

To enable email reports, configure the setup script when prompted or manually update the following environment variables in `docker-compose.yaml`:

```yaml
AIRFLOW__SMTP__SMTP_HOST: 'smtp.gmail.com'
AIRFLOW__SMTP__SMTP_PORT: '587'
AIRFLOW__SMTP__SMTP_USER: 'your-actual-email@gmail.com'
AIRFLOW__SMTP__SMTP_PASSWORD: 'your-gmail-app-password'
AIRFLOW__SMTP__SMTP_MAIL_FROM: 'your-actual-email@gmail.com'
```

For Gmail, you'll need to use an App Password instead of your regular password. 

## How to Create a Gmail App Password

To use Gmail for sending email notifications from the ETL Weather App, you need to set up an App Password. This is a security requirement for Google accounts, especially if you have 2-Factor Authentication enabled.

### Step-by-Step Instructions:

1. **Enable 2-Step Verification (if not already enabled)**:
   - Go to your [Google Account Security Settings](https://myaccount.google.com/security)
   - Select "2-Step Verification" and follow the steps to turn it on

2. **Generate an App Password**:
   - Go to [App Passwords](https://myaccount.google.com/apppasswords) (you must have 2-Step Verification enabled to see this option)
   - Select "Mail" from the app dropdown
   - Select "Other (Custom name)" from the device dropdown
   - Enter "ETL Weather App" as the name
   - Click "Generate"

3. **Copy the Generated Password**:
   - Google will display a 16-character password
   - Copy this password - it will only be shown once
   - Use this password in your ETL Weather App configuration

4. **Configure ETL Weather App**:
   - When running the setup script, choose "y" when asked if you want to configure email
   - Enter your Gmail address when prompted
   - Enter the App Password (not your regular Gmail password) when prompted for password

### Troubleshooting:

- **App Password Not Working**: Make sure 2-Step Verification is enabled on your Google account
- **Email Sending Fails**: Check that you're using the correct app password and not your regular account password
- **Gmail Blocks the App**: You might need to allow "less secure apps" in your Google account settings
- **Missing App Passwords Option**: This means you don't have 2-Step Verification enabled

### Security Note:

The App Password gives full access to your Gmail account, so treat it like your regular password. The ETL Weather App stores this password in the docker-compose.yaml file, so ensure you secure this file appropriately.

### Schedule

The default schedule is daily. To change it, modify the `schedule_interval` parameter in `dags/etl_weather.py`:

```python
with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',  # Change this to your desired schedule
         catchup=False) as dags:
```

## Usage

1. In the Airflow UI, find the `weather_etl_pipeline` DAG
2. Enable the DAG by toggling the switch on the left
3. Trigger the DAG manually for an immediate run, or wait for the scheduled execution
4. View the task logs to see the progress of the ETL process
5. Check the output files in the `/opt/airflow/dags/output/` directory inside the container

### Testing the Pipeline

To test the ETL pipeline immediately:

1. **Open the Airflow UI** at http://localhost:8082
2. **Find the DAG** named `weather_etl_pipeline`
3. **Click the "Play" button** (Trigger DAG) in the Actions column
4. **Monitor the execution** in the Graph or Grid view
5. **Check task logs** by clicking on a task and selecting "Log"

### Expected Output

After a successful run, you should see:

1. **Files in the output directory**:
   ```bash
   docker-compose -f docker-compose.yaml exec airflow-scheduler ls -la /opt/airflow/dags/output/
   ```

2. **Task success in the Airflow UI**:
   - `extract_weather_data`: Successfully retrieved data from Open-Meteo API
   - `transform_weather_data`: Successfully processed the weather data
   - `prepare_email_content`: Generated the HTML report
   - `save_weather_report`: Saved files to the output directory
   - `send_weather_email`: Sent email (if configured properly)

## File Outputs

The ETL pipeline generates two types of output files:

1. **HTML Reports**: `/opt/airflow/dags/output/weather_report_[TIMESTAMP].html`
   - Contains a formatted weather report with daily forecasts
   - Includes temperature, precipitation, and weather condition descriptions
   - Same content that's sent in email notifications

2. **JSON Data**: `/opt/airflow/dags/output/weather_data_[TIMESTAMP].json`
   - Contains the raw transformed weather data in JSON format
   - Includes all weather metrics (temperature, precipitation, wind speed, etc.)
   - Useful for further data processing or analysis
   - Sample structure:
     ```json
     {
       "location": "India",
       "forecast_date": "2025-09-07",
       "daily_data": [
         {
           "date": "2025-09-07",
           "temperature_max": 22.5,
           "temperature_min": 14.2,
           "precipitation_sum": 2.4,
           "weather_code": 61,
           "weather_description": "Light rain"
         },
         // Additional days...
       ]
     }
     ```

## Email Notifications

When email is properly configured, the ETL pipeline sends HTML-formatted email notifications containing:

1. **Daily Weather Report**: Same content as the HTML files
2. **Location Information**: City and country for the weather data
3. **Forecast Period**: Date range of the weather forecast
4. **Weather Metrics**: Temperature, precipitation, and weather conditions
5. **Generation Timestamp**: When the report was created

Emails are sent to the address configured in the `EMAIL_RECIPIENT` variable in `dags/etl_weather.py`. 
The email subject follows the format: "Weather Report for [LOCATION] - [DATE]"

To view these files from your host system:

```bash
docker-compose -f docker-compose.yaml exec airflow-scheduler cat /opt/airflow/dags/output/weather_data_[TIMESTAMP].json
```

## Troubleshooting

- **Email Sending Fails**: If email sending fails, check your SMTP credentials. The app will still save data to files even if email sending fails.
- **API Connection Issues**: Ensure the container has internet access to reach the Open-Meteo API.
- **Missing Output Directory**: The DAG will create the output directory if it doesn't exist, but you can manually create it:
  ```bash
  docker-compose -f docker-compose.yaml exec airflow-scheduler mkdir -p /opt/airflow/dags/output
  ```

## License

This project is licensed under the terms of the included LICENSE file.

## Acknowledgements

- Weather data provided by [Open-Meteo API](https://open-meteo.com/)
- Built with [Apache Airflow](https://airflow.apache.org/)
