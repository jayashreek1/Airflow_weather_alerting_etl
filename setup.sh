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
  
  # Update email settings in docker-compose.yaml
  sed -i '' "s/AIRFLOW__SMTP__SMTP_USER: 'your-actual-email@gmail.com'/AIRFLOW__SMTP__SMTP_USER: '$email_address'/g" docker-compose.yaml
  sed -i '' "s/AIRFLOW__SMTP__SMTP_PASSWORD: 'your-gmail-app-password'/AIRFLOW__SMTP__SMTP_PASSWORD: '$email_password'/g" docker-compose.yaml
  sed -i '' "s/AIRFLOW__SMTP__SMTP_MAIL_FROM: 'your-actual-email@gmail.com'/AIRFLOW__SMTP__SMTP_MAIL_FROM: '$email_address'/g" docker-compose.yaml
  
  # Update recipient email in the DAG file
  sed -i '' "s/EMAIL_RECIPIENT = 'your-actual-email@gmail.com'/EMAIL_RECIPIENT = '$email_address'/g" dags/etlweather.py
  
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
  echo "Learn more: https://support.google.com/accounts/answer/185833"
fi