# Finance Tracker

## Overview

**Finance Tracker** is a personal finance management system which allows users to track transactions, manage budgets, upload financial data, and visualize analytics via a React-based dashboard.

The backend is built with **Django and Django REST Framework** and includes secure authentication, ETL processing for uploaded data, comprehensive dashboards, and automated tests. The frontend dashboard provides an analytics of income, expenses, savings, and budget utilization.

---

## Features

* **Authentication & Authorization**

  * JWT-based login and token refresh
  * Role-based permissions (`user` and `admin`)
* **Transactions Management**

  * Create, read, update, delete income and expense transactions
  * Filter transactions by category or type
  * Order transactions by date or amount
* **File Upload & ETL**

  * Upload CSV or Excel files of transactions
  * Automatic ETL processing:

    * Cleans invalid dates
    * Normalizes categories
    * Determines transaction type based on amount
* **Budgets**

  * Manage monthly or yearly budgets per category
  * Prevent overlapping budgets
  * Calculate spent, remaining amounts, and percentage used
* **Dashboard Analytics**

  * Monthly and yearly aggregation of income, expenses, and savings
  * Key Performance Indicators (KPIs):

    * Total income
    * Total expenses
    * Net savings
    * Budget utilization percentage
* **Automated Tests**

  * Authentication, transactions, budgets, dashboard analytics, and file uploads
* **Swagger/OpenAPI Documentation**

  * Interactive API documentation for testing and integration
* **Dockerized**

  * Backend, frontend, database, and Nginx containerized for easy setup

* **React Dashboard**

  * Interactive charts using Chart.js (Line, Bar, Pie, Doughnut)
  * Switch between monthly and yearly analytics
  * Visualizes income, expenses, savings, and budget utilization

---

## Architecture

```
[React Frontend Dashboard] <--> [Django REST API] <--> [PostgreSQL Database]
                                        ^
                                        |
                                [ETL File Upload]
```

* **Django API**: Handles transactions, budgets, dashboards, and authentication.
* **ETL Pipeline**: Processes uploaded CSV/XLSX files for transactions.
* **React Frontend**: Displays analytics and charts.
* **PostgreSQL**: Stores all data.

---

## Tech Stack

**Backend**

* Python 3.11
* Django 4.x
* Django REST Framework
* PostgreSQL
* drf-spectacular for API docs

**Frontend**

* React 18
* Chart.js

**DevOps / Tools**

* Docker & Docker Compose
* Nginx for serving frontend
* Automated tests with Django/DRF TestCase
* GitHub Actions (for CI/CD)

---

## Environment Setup

Create a `.env` file with the following variables:

```
POSTGRES_USER=finance_user
POSTGRES_PASSWORD=password
POSTGRES_DB=finance_db
SECRET_KEY=your_django_secret_key
DEBUG=True
```

---

## Run with Docker

```bash
docker-compose up --build
```

* Backend API: `http://localhost:8000/`
* Swagger Docs: `http://localhost:8000/api/docs/`
* Frontend Dashboard via Nginx: `http://localhost/`

---

## API Endpoints Overview

| Endpoint                             | Method              | Description                                |
| ------------------------------------ | ------------------- | ------------------------------------------ |
| `/api/auth/register/`                | POST                | Register a new user                        |
| `/api/auth/login/`                   | POST                | Obtain JWT tokens                          |
| `/api/auth/token/refresh/`           | POST                | Refresh JWT access token                   |
| `/api/transactions/dashboard/`       | GET                 | Retrieve KPIs and monthly/yearly analytics |
| `/api/transactions/upload/`          | POST                | Upload CSV/XLSX financial data             |
| `/api/transactions/monthly-expense/` | GET                 | Monthly expense summary                    |
| `/api/categories/`                   | GET/POST/PUT/DELETE | Manage categories                          |
| `/api/budgets/`                      | GET/POST/PUT/DELETE | Manage budgets                             |

> Full API documentation available at `/api/docs/` via Swagger UI.

---

## ETL Pipeline

Defined in `transactions/etl/transform.py`

Cleans and transforms uploaded CSV/XLSX files:

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

* Authentication (`test_auth.py`)
* Transactions (`test_transactions.py`)
* Budgets (`test_budget.py`)
* Dashboard analytics (`test_dashboard.py`)
* File uploads and ETL (`test_upload.py`)

---


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and commit
4. Push branch and open a Pull Request

---


## License

MIT License. See LICENSE file for details.

Manage, track, and visualize your finances efficiently with Finance Tracker – backend-first, production-ready, and fully dockerized.

