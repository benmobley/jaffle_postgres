# 🛒 Olist Analytics Pipeline

Modern e-commerce analytics pipeline transforming Olist Brazilian dataset into actionable insights using **dbt**, **PostgreSQL**, and **Streamlit**.

## 📊 What This Does

Transforms raw e-commerce data into clean, tested analytics models:

- **Staging**: Clean customer, order, and payment data
- **Marts**: Dimensional models (customers, orders) + key metrics (revenue, cancellation rates)
- **Dashboard**: Interactive Streamlit dashboard for business KPIs

## 🔧 Tech Stack

| Component           | Technology     |
| ------------------- | -------------- |
| **Transformations** | dbt (SQL)      |
| **Database**        | PostgreSQL     |
| **Orchestration**   | Docker Compose |
| **Visualization**   | Streamlit      |
| **CI/CD**           | GitHub Actions |

## 🚀 Quick Start

1. **Start all services**

   ```bash
   docker-compose up -d
   ```

2. **Run dbt pipeline**

   ```bash
   ./run_pipeline.sh
   ```

   Or manually:

   ```bash
   docker-compose run --rm dbt dbt deps
   docker-compose run --rm dbt dbt seed
   docker-compose run --rm dbt dbt run
   docker-compose run --rm dbt dbt test
   ```

3. **Open dashboard**
   - Navigate to `http://localhost:8501`
   - Interactive Streamlit dashboard with multiple views

## 📈 Data Models

### Architecture

```
Raw Seeds → Staging Models → Dimensional & Fact Tables → Analytics Marts
```

### Key Models

- `dim_customer` - Customer attributes
- `fact_orders` - Order transactions with totals
- `monthly_revenue` - Revenue trends over time
- `top_customers` - Customer lifetime value rankings
- `cancellation_rate` - Order cancellation metrics

## ✅ Data Quality

Comprehensive testing ensures data reliability:

- **Uniqueness** & **completeness** checks on all primary keys
- **Referential integrity** between fact/dimension tables
- **Business logic** validation (positive amounts, valid statuses)
- **Type checking** and value constraints

## 🏗️ Project Structure

```
models/
├── staging/          # Clean raw data
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── stg_payments.sql
└── mart/             # Business-ready tables
    ├── dim_customer.sql
    ├── fact_orders.sql
    ├── monthly_revenue.sql
    ├── top_customers.sql
    └── cancellation_rate.sql
```

## 📊 Dashboard Features

The Streamlit dashboard includes four main views:

### 📈 Overview

- Key performance indicators (KPIs)
- Total revenue, customers, orders, average order value
- Quick trend charts for revenue and cancellation rates

### 💰 Revenue Analysis

- Monthly revenue trends and statistics
- Growth rate analysis
- Revenue distribution insights

### 👥 Customer Analysis

- Top customers by lifetime spend
- Customer distribution by state
- Spending behavior analysis

### 📦 Order Analysis

- Cancellation rate trends
- Order volume vs cancellations
- Payment conversion metrics

## 🐳 Docker Services

The application runs in containers:

- **PostgreSQL**: Database (port 5432)
- **dbt**: Data transformation service
- **Streamlit**: Interactive dashboard (port 8501)

## 🔄 CI/CD

Automated testing runs on every push:

- **SQL validation** with SQLFluff
- **dbt parse** & **test** execution
- **Documentation** generation
- **Pre-commit hooks** for code quality

## 📊 Lineage Screenshot

![dbt Lineage Graph](https://github.com/user-attachments/assets/screenshot-lineage.png)

The lineage graph shows the complete data flow from raw Olist datasets through staging models to final business marts and analytics tables.
