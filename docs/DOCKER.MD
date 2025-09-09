## ☁️ Infrastructure as Code (IaC) – Why It Matters?

**What is IaC?**  
Infrastructure as Code is the practice of **defining and managing infrastructure using code** instead of manual setup.

**Why is it important?**
- ✅ **Consistency** – Same environment every time
- ✅ **Automation** – No more manual server setup
- ✅ **Scalability** – Easy to replicate for multiple environments

**Examples:**
- Dockerfiles (for containers)
- Terraform (for cloud infra)
- Kubernetes manifests (for orchestration)

**In this session:**  
Docker acts as IaC – we define **Airflow setup in code** so it runs anywhere!

# 🐳 What is Docker? (Explained Simply)

## ✅ Start with a Relatable Analogy
**Imagine you are organizing a college event.**
- You need a **stage, lights, sound system, and volunteers** to run the show.
- If every college fest required **buying everything from scratch**, it would be **time-consuming and inconsistent**.
- Instead, what if you had a **ready-made event kit** where everything is pre-packed and works the same every time?
- You just **unpack it and start the show**.

👉 **Docker is like that event kit for software.**  
It **packages everything** your app needs (code, libraries, configurations) into a **container** so it works **anywhere**.

---

## ✅ The Problem Docker Solves
- **Before Docker:**  
  Developer writes code → Works on their laptop → **Fails on server** (different OS, missing libraries).

- **With Docker:**  
  App runs **inside a container with all dependencies** → Works the **same on any machine**.

---

## ✅ Real-World Example
**Group Project Scenario:**
- You use **Windows**, your friend uses **Mac**, another uses **Linux**.
- Without Docker: Hours wasted fixing setup issues.
- With Docker:
  ```bash
  docker run hello-world