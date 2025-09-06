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
ETLWeather/
├── dags/                    # Airflow DAG files
│   ├── etlweather.py        # Main ETL pipeline DAG
│   └── output/              # Directory where weather reports are saved
├── docker-compose.yaml      # Docker Compose configuration
├── Dockerfile               # Docker image definition
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
   git clone https://github.com/krishnaik06/ETLWeather.git
   cd ETLWeather
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

You can change the location for which weather data is fetched by modifying the latitude and longitude variables in `dags/etlweather.py`:

```python
# Latitude and longitude for the desired location (London by default)
LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
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

For Gmail, you'll need to use an App Password instead of your regular password. You can generate one at https://myaccount.google.com/apppasswords.

### Schedule

The default schedule is daily. To change it, modify the `schedule_interval` parameter in `dags/etlweather.py`:

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

## File Outputs

The ETL pipeline generates two types of output files:

1. **HTML Reports**: `/opt/airflow/dags/output/weather_report_[TIMESTAMP].html`
2. **JSON Data**: `/opt/airflow/dags/output/weather_data_[TIMESTAMP].json`

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
