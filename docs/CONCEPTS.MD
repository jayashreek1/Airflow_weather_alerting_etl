# Airflow Core Concepts

## ✅ DAG (Directed Acyclic Graph)
- A collection of tasks arranged in order
- Like a **recipe** for a dish
- No circular dependencies

Eg: - Like a **recipe** for a dish. Has a list of ingredients to prepare a dish

---

## ✅ Operator
- Operator are templates for defining the work that needs to be done. Each operator is designed to perform a specific type of action
- Examples:
    - PythonOperator
    - BashOperator
    - EmailOperator

Eg: 
- If DAG = Recipe, **Operator = Instruction in recipe**

---

## ✅ Task & Task Instance
- When an operator is assigned to a DAG → becomes a **task**
- A task running at a specific time → **task instance**

---
