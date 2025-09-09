#!/bin/bash

echo "Starting ETL Weather setup..."

# Function to check if Docker is running
check_docker() {
  if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
  fi
}

# Check if Docker is running
check_docker
echo "✅ Docker is running"

# Create or update .env file if it doesn't exist
if [ ! -f .env ]; then
  cat > .env << EOF
AIRFLOW_UID=$(id -u)

# Email settings
AIRFLOW_SMTP_USER=your-email@gmail.com
AIRFLOW_SMTP_PASSWORD=your-app-password

# You can add other sensitive environment variables here
EOF
  echo "✅ Created .env file - edit it with your email and password"
  echo "   For Gmail, use an App Password (see README.md)"
else
  echo "✅ Using existing .env file"
fi

# Load variables from .env
source .env

# Check if email is configured
if [[ -n "$AIRFLOW_SMTP_USER" && "$AIRFLOW_SMTP_USER" != "your-email@gmail.com" ]]; then
  # Set the environment variable for the containers
  export AIRFLOW_EMAIL_RECIPIENT=$AIRFLOW_SMTP_USER
  
  # Update EMAIL_RECIPIENT in utils.py (the active file being used)
  if [ -f dags/tasks/utils.py ]; then
    sed -i '' "s/EMAIL_RECIPIENT = os.getenv('AIRFLOW_EMAIL_RECIPIENT', '.*')/EMAIL_RECIPIENT = os.getenv('AIRFLOW_EMAIL_RECIPIENT', '$AIRFLOW_SMTP_USER')/g" dags/tasks/utils.py
  fi
  
  echo "✅ Email configured: $AIRFLOW_SMTP_USER"
else
  echo "⚠️  Email not configured in .env file"
  echo "   Weather data will be saved to files but no emails will be sent"
fi

echo "Starting Airflow services..."
docker-compose down -v
docker-compose up -d

echo "✅ Airflow is starting up"
echo "   Access the Airflow UI at http://localhost:8082"
echo "   Username: admin / Password: admin"