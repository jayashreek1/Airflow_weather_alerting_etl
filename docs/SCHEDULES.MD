# ⏲️ Task Scheduling Fundamentals (Quick Catch-Up)

This section will help you understand **scheduling concepts** and why we need tools like **Apache Airflow**.

---

## 📌 1. What is Task Scheduling?
Task scheduling is about **running tasks automatically at a specific time or interval**.  
Instead of manually starting scripts, you create rules to automate workflows.

Examples:
- Run a script every day at midnight
- Send weekly email reports on Monday mornings

---

## ⏳ 2. Key Concepts

| Concept               | Definition                                            | Example                                   |
|----------------------|------------------------------------------------------|-------------------------------------------|
| **Task**             | A single job or script                               | Python script to extract data             |
| **Trigger**          | The event or time that starts a job                  | Every 24 hours at midnight                |
| **Interval**         | Frequency of job execution                           | Every hour, daily, weekly                 |
| **Retry Policy**     | Rules for rerunning failed tasks                     | Retry 3 times with 5-min delay            |

---

## 🕐 3. Traditional Scheduling with Cron

**Cron** is a Linux utility for time-based scheduling.  
A cron expression looks like:
0 0 * * *   #  - Run at midnight every day

| Field         | Example Value | Meaning            |
|--------------|--------------|-------------------|
| Minute (0-59)| 0            | At :00 minute     |
| Hour (0-23)  | 0            | At midnight       |
| Day of Month | *            | Every day         |
| Month        | *            | Every month       |
| Day of Week  | *            | Every day of week |

---
