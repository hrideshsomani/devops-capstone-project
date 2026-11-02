# DevOps Capstone Project

[![Build Status](https://github.com/hrideshsomani/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/hrideshsomani/devops-capstone-project/actions/workflows/ci-build.yaml)

## Project Overview

The **DevOps Capstone** project is a Customer Accounts Microservice — a RESTful API service built with Python and Flask that manages customer account records. It provides full CRUD (Create, Read, Update, Delete) operations and is designed with modern DevOps practices including CI/CD pipelines, containerization with Docker, and deployment on Kubernetes.

## Features

- ? RESTful API for Customer Account Management (CRUD)
- ? Automated Testing with 
osetests and code coverage
- ? Continuous Integration via GitHub Actions
- ? Security Headers via Flask-Talisman & CORS Policies
- ? Containerized with Docker
- ? Deployed on Kubernetes
- ? CD Pipeline with Tekton

## Tech Stack

| Layer        | Technology               |
|--------------|--------------------------|
| Language     | Python 3.9               |
| Framework    | Flask                    |
| Database     | SQLAlchemy / SQLite      |
| Testing      | nosetests, coverage      |
| Linting      | Flake8, Pylint           |
| CI/CD        | GitHub Actions, Tekton   |
| Container    | Docker                   |
| Orchestration| Kubernetes (OpenShift)   |
| Security     | Flask-Talisman, Flask-CORS |

## API Endpoints

| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| POST   | /accounts         | Create a new account     |
| GET    | /accounts         | List all accounts        |
| GET    | /accounts/{id}    | Read a single account    |
| PUT    | /accounts/{id}    | Update an account        |
| DELETE | /accounts/{id}    | Delete an account        |
| GET    | /health           | Health check             |

## Running Locally

`ash
# Install dependencies
pip install -r requirements.txt

# Run the service
flask run

# Run tests
nosetests
`

## Docker

`ash
docker build -t customer-accounts .
docker run -p 8080:8080 customer-accounts
`

## Kubernetes

`ash
kubectl apply -f k8s/
kubectl get pods
kubectl get services
`

## License

Apache 2.0 License
