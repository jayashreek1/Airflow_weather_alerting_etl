# 🛠️ Data Engineering - Quick Revamp

This is a quick primer to get you ready for **Apache Airflow**. It covers the essential Data Engineering concepts you'll need.

---

## 📌 1. What is Data Engineering?
Data Engineering is about **designing, building, and maintaining systems** that move, process, and store data.  
Think of it as the **plumbing of data** – getting raw data from multiple sources and making it usable for analytics, ML, or apps.

---

## 📊 2. Types of Data
| Type             | Example                          | Storage         |
|------------------|---------------------------------|----------------|
| **Structured**   | Tables, SQL rows/columns        | RDBMS (MySQL)  |
| **Semi-structured** | JSON, XML, Logs             | Data Lakes     |
| **Unstructured** | Images, Videos, Text            | Object Storage |

---

## 🔄 3. ETL vs ELT

| Process | ETL (Extract → Transform → Load)            | ELT (Extract → Load → Transform)          |
|---------|--------------------------------------------|------------------------------------------|
| Flow    | Clean before loading into DB                | Load raw data, transform in warehouse    |
| Use Case| Legacy systems, smaller data volumes       | Modern cloud-based pipelines             |
| Example | Clean CSV → Load to SQL Server             | Dump raw data → Transform with BigQuery  |

---

## ⏱️ 4. Batch vs Stream Processing
- **Batch Processing**: Process data in scheduled batches (e.g., hourly, daily).  
  _Example: Generate daily sales reports at midnight._
- **Stream Processing**: Process events **in real-time** as they arrive.  
  _Example: Fraud detection while swiping a credit card._

Airflow is **mostly used for batch workflows**.

---

## 🌐 5. Common Tools in Data Engineering
| Category             | Examples                       |
|----------------------|--------------------------------|
| Databases            | PostgreSQL, MySQL, Snowflake   |
| Data Lakes           | Amazon S3, Google Cloud Storage|
| Processing Engines   | Spark, Pandas, DBT             |
| Orchestration Tools  | Apache Airflow, Prefect, Luigi |
