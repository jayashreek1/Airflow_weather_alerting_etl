# Core Components

## Metadata Database
- Stores task data, status, and user roles.

## Scheduler
- Decides **when to run tasks**.
- Ensures correct order (like an alarm clock).
- DAG File Processor parses DAGs and stores metadata.

## Executor
- Determines **how and where tasks run**.
- Supports sequential, parallel, cloud, and on-prem execution.

## API Server
- Provides endpoints for task management and monitoring.

## Worker
- Executes tasks assigned by the scheduler.

## Queue
- Manages task list and execution order.
- Can be internal or external (e.g., RabbitMQ).

## Triggerer
- Handles deferrable tasks dependent on external events.