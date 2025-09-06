FROM apache/airflow:2.8.1

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configure email settings
ENV AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
ENV AIRFLOW__SMTP__SMTP_PORT=587
ENV AIRFLOW__SMTP__SMTP_USER=test@example.com
ENV AIRFLOW__SMTP__SMTP_PASSWORD=your-app-password
ENV AIRFLOW__SMTP__SMTP_MAIL_FROM=test@example.com
ENV AIRFLOW__SMTP__SMTP_STARTTLS=True
ENV AIRFLOW__SMTP__SMTP_SSL=False
