{{ config(
    materialized='table',
    description='Monthly revenue aggregation. Sums total order amounts grouped by month.'
) }}

with monthly_totals as (
    select
        date_trunc('month', order_date)::date as revenue_month,
        sum(total_amount) as revenue
    from {{ ref('fact_orders') }}
    group by date_trunc('month', order_date)
)

select
    revenue_month,
    round(revenue, 2) as revenue
from monthly_totals
order by revenue_month desc
