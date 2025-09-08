# Airflow Core Concepts

## ✅ DAG (Directed Acyclic Graph)
- A collection of tasks arranged in order
- Like a **recipe** for a dish
- No circular dependencies

---

## ✅ Operator
- A single, **idempotent** task
- Examples:
    - PythonOperator
    - BashOperator
    - EmailOperator
- If DAG = Recipe, **Operator = Instruction in recipe**

---

## ✅ Task & Task Instance
- When an operator is assigned to a DAG → becomes a **task**
- A task running at a specific time → **task instance**

---

## ✅ Workflow
- The complete process (e.g., ETL)

---

### ✅ Idempotency
- A task should produce the same result even if run multiple times

---

### ✅ Our ETL DAG Concepts:
- **DAG:** `weather_etl_pipeline`
- **Operators:** Python functions for extract, transform, save
- **Task Instances:** Each daily run of extract/transform/save