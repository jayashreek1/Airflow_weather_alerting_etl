# Airflow Architecture

## Single Node
- Smaller workflows.
- Simple setup, limited scalability.

## Multi Node
- Larger workflows for production.
- Scalable, reliable, performant.
- Handles complex workflows.

## How Airflow Works
- DAGs define tasks.
- Scheduler triggers tasks based on time/dependencies.
- Executor decides execution mode (parallel/sequential).
- Workers perform the tasks.
- Metadata database tracks status and logs.