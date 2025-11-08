# Olist E-commerce Analytics Pipeline (dbt + Postgres + Metabase)

This project builds an end-to-end analytics pipeline on the **Olist Brazilian e-commerce dataset** using **dbt**, **Postgres**, and **Metabase**.  

Raw CSVs are loaded into Postgres, transformed with dbt into clean **staging**, **dimension**, **fact**, and **metrics** models, and then visualized in a simple KPI dashboard.

---

## Tech Stack

- **dbt (dbt-postgres)** – SQL transformations, tests, and documentation  
- **PostgreSQL** – data warehouse  
- **Python + venv** – environment management  
- **Docker + Metabase** – lightweight BI/dashboard  
- **Olist Brazilian E-commerce dataset** – public source data (customers, orders, items, payments)

---

## Data & Modeling

Source CSVs (seeds):

- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`

dbt models follow a layered approach:

- **Raw / Seeds**: loaded into `analytics_raw.*`
- **Staging** (`models/staging/olist/…`)
  - `stg_olist_customers`
  - `stg_olist_orders`
  - `stg_olist_order_items`
  - `stg_olist_payments`
- **Marts** (`models/marts/olist/…`)
  - `dim_olist_customer`
  - `fact_olist_orders`
- **Metrics** (`models/marts/olist/metrics/…`)
  - `monthly_revenue` – revenue by month
  - `cancellation_rate` – order cancellation rate by month
  - `top_customers` – top customers by lifetime spend

Lineage example:

<img width="1875" height="892" alt="image" src="https://github.com/user-attachments/assets/04bc1ed1-071a-4113-a096-4dc920a1b027" />

---

## Data Quality & Testing

dbt tests are used to keep the models trustworthy:

- `unique` / `not_null` on primary keys:  
  - `customer_id`, `order_id`, etc.  
- Basic integrity checks on metrics:
  - `monthly_revenue.month` is unique / not null  
  - `cancellation_rate.cancellation_rate` is not null  
  - `top_customers.customer_id` is unique / not null  

Run all models + tests:

```bash
dbt build


## Dashboard (Metabase)

A Metabase dashboard called “Olist KPIs” exposes three core KPIs:
	1.	Monthly Revenue – line chart of revenue by month
	2.	Cancellation Rate – line chart showing cancellation rate over time
	3.	Top Customers by Spend – horizontal bar chart for highest-spending customers

<img width="1117" height="934" alt="image" src="https://github.com/user-attachments/assets/0aac80c2-e1d8-492b-bd2d-872cbca991dd" />


## Getting Started

1. Clone & Set up environment

  git clone <your-repo-url>
  cd jaffle_postgres   # or your project directory
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install dbt-postgres


2. Postgres & dbt profile

Create a Postgres database (if you don't already have one)

  createdb jaffle   # or use psql to CREATE DATABASE jaffle

Create ~./dbt/profiles.yml:

  jaffle_postgres:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: postgres
      password: postgres
      dbname: jaffle
      schema: analytics
      threads: 4

Create the raw schema once:

  PGPASSWORD=postgres psql -h localhost -U postgres -d jaffle \
  -c 'create schema if not exists analytics_raw;'


3. Run dbt

  From the dbt project directory:

  dbt debug       # check connection
  dbt seed        # load raw + Olist CSVs
  dbt build       # run models + tests
  dbt docs serve  # optional: open docs + lineage graph


4. Run Metabase & Dashboard

  Spin up Metabase in Docker (connecting to your local Postgres)

  docker run -d --name jaffle_metabase -p 3000:3000 metabase/metabase

  In your browser go to http://localhost:3000 and:
	1.	Create an admin user.
	2.	Add a PostgreSQL database:
	•	Host: host.docker.internal
	•	Port: 5432
	•	Database: jaffle
	•	User / Password: postgres / postgres
	•	Schema: analytics
	3.	Create three questions using:
	•	analytics.monthly_revenue
	•	analytics.cancellation_rate
	•	analytics.top_customers
	4.	Add them to a dashboard named “Olist KPIs”.


## Project Structure (key folders)

  jaffle_postgres/
  dbt_project.yml
  profiles.yml (local, in ~/.dbt)
  models/
    staging/
      olist/
        stg_olist_customers.sql
        stg_olist_orders.sql
        stg_olist_order_items.sql
        stg_olist_payments.sql
    marts/
      olist/
        dim_olist_customer.sql
        fact_olist_orders.sql
        metrics/
          monthly_revenue.sql
          cancellation_rate.sql
          top_customers.sql
  seeds/
    olist/
      olist_customers_dataset.csv
      olist_orders_dataset.csv
      olist_order_items_dataset.csv
      olist_order_payments_dataset.csv

## Future Improvements

  	•	Add incremental models for large Olist tables
  	•	Add snapshots for slowly changing customer attributes
  	•	Automate dbt build via GitHub Actions CI
  	•	Add more product-level metrics (e.g., category-level revenue, repeat purchase behavior)

