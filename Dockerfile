FROM apache/airflow:2.8.1

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Note: Email settings are configured in docker-compose.yaml
