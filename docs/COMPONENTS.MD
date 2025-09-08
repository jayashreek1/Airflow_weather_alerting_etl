# Airflow Core Components

## ✅ 1. Metadata Database
- Stores:
    - Task states
    - DAG runs
    - Users & roles
- Example: PostgreSQL, MySQL

---

## ✅ 2. Scheduler
- Decides **when to run tasks**
- Ensures correct order
- Parses DAG files and stores metadata in DB

---

## ✅ 3. Executor
- Decides **where and how** to run tasks:
    - Sequential
    - Local
    - Celery
    - Kubernetes

---

## ✅ 4. API Server
- Provides REST endpoints for task operations

---

## ✅ 5. Workers
- Actually **execute tasks**

---

## ✅ 6. Queue
- Holds tasks waiting to run
- Can be internal or external (RabbitMQ, Redis)

---

## ✅ 7. Triggerer
- Handles **deferrable operators** (long waits, external events)

---

### ✅ Mapping to Our DAG
| Component    | Role in Our ETL Example |
|-------------|---------------------------|
| Metadata DB | Stores task states for `extract`, `transform`, `save`, `email` |
| Scheduler   | Runs DAG daily at 6 AM |
| Executor    | Decides task execution strategy |
| Worker      | Executes API call, data transformation |
| Queue       | Maintains task order |