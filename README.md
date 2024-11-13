# Project Scaffold

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Scaffold](https://img.shields.io/badge/scaffold-orange.svg)](https://www.python.org/downloads/)


This project provides a scaffold for lightweight web applications in FastAPI, supporting background task processing with Celery. It’s ideal for applications with a simple interface but requiring background processing for resource-intensive tasks. The scaffold includes Docker configuration for streamlined deployment.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Initial Setup](#initial-setup)
- [Using This Project as a Template](#using-this-project-as-a-template)
- [Project Structure](#project-structure)
- [Adding New Tasks](#adding-new-tasks)
- [Monitoring Background Tasks](#monitoring-background-tasks)
- [Configuration Details](#configuration-details)



## Features

- **Lightweight Web Interface**: Fast, responsive web application.
- **Background Task Processing**: Uses Celery for efficient background task execution.
- **Dockerized Environment**: Simplifies setup and deployment using Docker.
- **Monitoring with Flower**: Real-time monitoring of background tasks with Flower.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Docker
- Python 3.12

### Initial Setup

1. Clone the repository:

    ```sh
    git clone <repository_url>
    cd <repository_name>
    ```

2. Configure Environment Variables:
    - Copy `.env-test` to `.env` and fill in the necessary details, including sensitive information like passwords. This approach keeps sensitive information secure.

3. Build and Start the Containers:
    - Use Docker Compose to build and start the environment:

    ```sh
    docker-compose -f docker-compose.dev.yml up -d --build
    ```

This will start the following containers:
- **app**: The main web application accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **redis**: In-memory data store for task queues and cache.
- **worker**: Celery worker for background task processing.
- **flower**: Task monitoring app, accessible at [http://127.0.0.1:5555/](http://127.0.0.1:5555/)

## Using This Project as a Template

To use this project as a template for another project, follow these steps:

1. **Clone the Repository**: Clone the existing repository to your local machine.

    ```sh
    git clone <repository_url>
    ```

2. **Rename the Project Directory**: Rename the cloned project directory to your new project name.

    ```sh
    mv <repository_name> <new_project_name>
    ```

3. **Update Project Metadata**: Open the `pyproject.toml` file and update the project name, version, description, authors, repository, and homepage fields to reflect the new project details.

    ```toml
    [tool.poetry]
    name = "<new_project_name>"
    version = "0.1.0"
    description = "Description of the new project"
    authors = ["Your Name <your.email@example.com>"]
    ```

4. **Configure Environment Variables**: Copy the `.env-test` file to `.env` and fill in the necessary details, including sensitive information like passwords.

    ```sh
    cp .env-test .env
    ```

5. **Customize the README**: Update the `README.md` file to reflect the new project details, including the project name, description, and any specific instructions or information relevant to the new project.

6. **Install Dependencies**: Run `poetry install` to install the project dependencies.

    ```sh
    poetry install
    ```

7. **Build and Start the Containers**: Use Docker Compose to build and start the environment.

    ```sh
    docker-compose -f docker-compose.dev.yml up -d --build
    ```

8. **Modify the Codebase**: Make any necessary changes to the codebase to fit the requirements of the new project. This may include updating routes, templates, and background tasks.

9. **Commit and Push Changes**: Commit your changes to a new Git repository and push them to your version control system.

    ```sh
    git init
    git add .
    git commit -m "Initial commit for <new_project_name>"
    git remote add origin <new_repository_url>
    git push -u origin main
    ```

By following these steps, you can effectively use the existing project as a template for creating a new project.

## Project Structure

```
.
├── app/ # Main application directory
│ ├── __main__.py # Entry point for the web server
│ ├── router.py # Contains routing logic for the web app
│ ├── worker.py # Celery worker setup and task definitions
├── .env-test # Sample environment file
├── docker-compose.dev.yml # Docker Compose configuration for development
```


## Adding New Tasks

To add new background tasks, define them in `app/worker.py` and configure them to be executed by Celery.

1. Define the task:

    ```python
    @celery_app.task
    def my_task():
        # Task logic here
    ```

2. Call the task in your application code as needed:

    ```python
    my_task.delay()
    ```

## Monitoring Background Tasks

Flower provides a web interface for monitoring task status, failures, and performance. To access Flower, visit [http://127.0.0.1:5555/](http://127.0.0.1:5555/).

## Configuration Details

The Docker configuration (`docker-compose.dev.yml`) specifies each container’s role:
- **app**: Runs the FastAPI server.
- **worker**: Manages Celery tasks.
- **redis**: Acts as the message broker.
- **flower**: Monitors task queue in real-time.

Each container inherits settings from the `x-app` service for consistency. Redis is secured using a password stored in `.env`.

This README serves as a comprehensive guide to understanding, configuring, and extending the scaffold for new projects.
