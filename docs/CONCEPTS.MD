# Core Concepts

## DAG – Directed Acyclic Graph
- Collection of tasks organized by dependencies.
- No circular dependencies.
- Analogy: a recipe for a dish.

## Operator
- Represents a single, idempotent task.
- DAG = recipe, Operator = instruction.
- Examples: PythonOperator, BashOperator, SQLOperator, FileSensor.

## Task / Task Instance
- Specific instance of an operator in a DAG.
- Example: Operator = Add Salt, Task = Add Salt at 9:00 AM.

## Workflow
- Orchestration of multiple DAGs/tasks sequentially or in parallel.

## When Not to Use Airflow
- High-frequency, sub-minute scheduling.
- Real-time streaming (trading pipelines).
- Extremely large datasets in a single task.
- Simple linear workflows where cron jobs suffice.