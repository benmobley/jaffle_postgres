# 🛒 Olist Analytics Pipeline

Modern e-commerce analytics pipeline transforming Olist Brazilian dataset into actionable insights using **dbt**, **PostgreSQL**, and **Metabase**.

## 📊 What This Does

Transforms raw e-commerce data into clean, tested analytics models:

- **Staging**: Clean customer, order, and payment data
- **Marts**: Dimensional models (customers, orders) + key metrics (revenue, cancellation rates)
- **Dashboard**: Metabase visualizations for business KPIs

## 🔧 Tech Stack

| Component           | Technology     |
| ------------------- | -------------- |
| **Transformations** | dbt (SQL)      |
| **Database**        | PostgreSQL     |
| **Orchestration**   | Docker Compose |
| **Visualization**   | Metabase       |
| **CI/CD**           | GitHub Actions |

## 🚀 Quick Start

1. **Start services**

   ```bash
   docker-compose up -d
   ```

2. **Run dbt pipeline**

   ```bash
   dbt deps
   dbt seed
   dbt run
   dbt test
   ```

3. **Open dashboard**
   - Navigate to `http://localhost:3000`
   - Connect to PostgreSQL: host=`pg`, database=`jaffle`

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

## 🔄 CI/CD

Automated testing runs on every push:

- **SQL validation** with SQLFluff
- **dbt parse** & **test** execution
- **Documentation** generation
- **Pre-commit hooks** for code quality

## 📊 Lineage Screenshot

The lineage graph shows the complete data flow from raw Olist datasets through staging models to final business marts and analytics tables.
