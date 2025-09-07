#!/bin/bash

echo "Starting setup script..."

# Function to check if Docker is running
check_docker() {
  if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
  fi
}

# Check if Docker is running
echo "Checking if Docker is running..."
check_docker
echo "Docker is running."

# Ask about email configuration
read -p "Would you like to configure email settings? (y/n): " configure_email

if [ "$configure_email" = "y" ]; then
  # Get email address
  read -p "Enter your email address: " email_address
  
  # Get email password
  read -p "Enter your email password (for Gmail, use an App Password): " email_password
  echo ""
  echo "For information on how to create a Gmail App Password, see README.md"
  
  # Update .env file with the SMTP password
  grep -q "AIRFLOW_SMTP_PASSWORD" .env && sed -i '' "s/AIRFLOW_SMTP_PASSWORD=.*/AIRFLOW_SMTP_PASSWORD=$email_password/g" .env || echo "AIRFLOW_SMTP_PASSWORD=$email_password" >> .env
  
  # Update email settings in docker-compose.yaml
  sed -i '' "s/AIRFLOW__SMTP__SMTP_USER: 'give your email'/AIRFLOW__SMTP__SMTP_USER: '$email_address'/g" docker-compose.yaml
  sed -i '' "s/AIRFLOW__SMTP__SMTP_MAIL_FROM: 'your email'/AIRFLOW__SMTP__SMTP_MAIL_FROM: '$email_address'/g" docker-compose.yaml
  
  # Update recipient email in the DAG file
  sed -i '' "s/EMAIL_RECIPIENT = 'test@gmail.com'/EMAIL_RECIPIENT = '$email_address'/g" dags/etl_weather.py
  
  echo "Email settings configured."
else
  echo "Skipping email configuration."
  echo "Note: Weather data will still be saved to files but email reports will not be sent."
fi

echo "Starting Airflow services..."
docker-compose down -v
docker-compose up -d

echo "Airflow is starting up. Please wait a few moments..."
echo "You can access the Airflow web UI at http://localhost:8082"
echo "Username: admin"
echo "Password: admin"

if [ "$configure_email" = "y" ]; then
  echo ""
  echo "The weather report will be emailed to $email_address daily."
  echo "If using Gmail, make sure you're using an App Password."
fi