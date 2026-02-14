# Finance Tracker


![Build Status](https://github.com/barshakc/Finance-Tracker/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

**Finance Tracker** is a personal finance management system that allows users to track transactions, manage budgets, upload financial data, and visualize analytics via a React-based dashboard.

The backend is built with **Django and Django REST Framework** and includes secure authentication, ETL processing for uploaded data, comprehensive dashboards, and automated tests. The frontend dashboard provides analytics for income, expenses, savings, and budget utilization.

---

## Features

### Authentication & Authorization

* JWT-based login and token refresh
* Role-based permissions (`user` and `admin`)

### Transactions Management

* Create, read, update, delete income and expense transactions
* Filter transactions by category or type
* Order transactions by date or amount

### File Upload & ETL

* Upload CSV or Excel files of transactions
* Automatic ETL processing:

  * Cleans invalid dates
  * Normalizes categories
  * Determines transaction type based on amount
  * Converts negative amounts to expenses, positive to income
  * Drops invalid rows 

### Budgets

* Manage monthly or yearly budgets per category
* Prevent overlapping budgets
* Calculate spent, remaining amounts, and percentage used

### Dashboard Analytics

* Monthly and yearly aggregation of income, expenses, and savings
* Key Performance Indicators (KPIs):

  * Total income
  * Total expenses
  * Net savings
  * Budget utilization percentage

### Automated Tests

* Authentication tests
* Transactions tests
* Budget validation tests
* Dashboard analytics tests
* File upload and ETL tests

### API Documentation

* Swagger/OpenAPI documentation via `drf-spectacular`
* Interactive testing available at `/api/docs/`

### Dockerized Infrastructure

* Backend container (Django + Gunicorn)
* Frontend container (React build)
* PostgreSQL database container
* Nginx reverse proxy container

---

## Architecture

```
Client (Browser)
↓
Nginx (Reverse Proxy & Static Files)
↓
Gunicorn (WSGI Server)
↓
Django REST API
↓
PostgreSQL Database
```

ETL uploads are processed within the Django backend before persistence.

### Components

* **Nginx**

  * Serves React production build
  * Reverse proxies API requests to Django
  * Handles static files

* **Gunicorn**

  * Production-grade WSGI server
  * Manages worker processes

* **Django REST API**

  * Business logic
  * Authentication & authorization
  * ETL pipeline
  * Dashboard analytics

* **PostgreSQL**

  * Persistent relational database
  * Ensures transactional integrity for financial data

---

## Tech Stack

### Backend

* Python 3.11
* Django 4.x
* Django REST Framework
* PostgreSQL
* drf-spectacular (Swagger/OpenAPI)

### Frontend

* React 18
* Chart.js

### DevOps / Tools

* Docker & Docker Compose
* Nginx
* Gunicorn
* Django TestCase (automated testing)

---

## CI/CD

Uses GitHub Actions to automate backend tests, frontend build, and Docker image builds.

Required repository secrets:
* SECRET_KEY (Django secret key)
* VITE_API_URL (Frontend API URL)
* DOCKER_USERNAME / DOCKER_PASSWORD (Docker Hub credentials)

Workflow triggers on push or pull request to main and development.

## Environment Setup

Create a `.env` file:

```
POSTGRES_USER=finance_user
POSTGRES_PASSWORD=password
POSTGRES_DB=finance_db
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Run Locally with Docker

```bash
docker-compose up --build
```

Access:

* Backend API → [http://localhost:8000/](http://localhost:8000/)
* Swagger Docs → [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
* Frontend Dashboard → [http://localhost/](http://localhost/)

---


# 🚀 Deployment Guide

Finance Tracker is fully containerized and can be deployed to any Docker-compatible environment (VPS, cloud VM, or container platforms).

## Prerequisites

* Docker
* Docker Compose
* Git

Optional:

* Domain name
* Linux VPS (Ubuntu recommended)

---

## Production Deployment (Docker-Based)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/Finance-Tracker.git
cd Finance-Tracker
```

### 2️⃣ Create Production `.env`

```
POSTGRES_USER=finance_user
POSTGRES_PASSWORD=new_password
POSTGRES_DB=finance_db
SECRET_KEY=your_secure_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### 3️⃣ Start Containers

```bash
docker-compose up --build -d
```

### 4️⃣ Apply Migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5️⃣ Collect Static Files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### 6️⃣ Create Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Cloud Deployment Options

Because the project is Dockerized, it can be deployed to:

* Fly.io
* DigitalOcean
* AWS EC2
* Azure
* Railway
* Render

Deployment process:

1. Provision a server or container service
2. Install Docker & Docker Compose
3. Clone the repository
4. Configure `.env`
5. Run Docker Compose commands

---

## API Endpoints Overview

| Endpoint                             | Method | Description                    |
| ------------------------------------ | ------ | ------------------------------ |
| `/api/auth/register/`                | POST   | Register new user              |
| `/api/auth/login/`                   | POST   | Obtain JWT tokens              |
| `/api/auth/token/refresh/`           | POST   | Refresh JWT token              |
| `/api/transactions/dashboard/`       | GET    | Retrieve KPIs and analytics    |
| `/api/transactions/upload/`          | POST   | Upload CSV/XLSX financial data |
| `/api/transactions/monthly-expense/` | GET    | Monthly expense summary        |
| `/api/categories/`                   | CRUD   | Manage categories              |
| `/api/budgets/`                      | CRUD   | Manage budgets                 |

Full API documentation available at `/api/docs/`.

---

## ETL Pipeline

Defined in `transactions/etl/transform.py`:

* Converts dates to timezone-aware format
* Normalizes category names
* Determines transaction type (`EXPENSE` or `INCOME`)
* Converts negative amounts to expenses, positive to income
* Drops invalid rows and handles missing data gracefully

---

## Dashboard Highlights

* **Expense Trend**: Monthly/yearly expenses line chart
* **Income vs Expense**: Compare income and expenses over time
* **Savings Trend**: Track net savings
* **Income vs Expense vs Savings**: Pie chart summary
* **Budget vs Expenses**: Bar chart comparing budgets to actual expenses
* **Budget Utilization**: Doughnut chart showing used vs remaining budget

---

## Testing

Run all backend tests:

```bash
docker-compose run web python manage.py test
```

Test coverage includes:

* Authentication
* Transactions
* Budgets
* Dashboard analytics
* ETL file uploads

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push and open a Pull Request

---


## License

MIT License. See LICENSE file for details.

Manage, track, and visualize your finances efficiently with Finance Tracker – backend-first and fully dockerized.

