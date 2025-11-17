{{ config(
    materialized='table',
    description='Monthly cancellation rate analysis. Tracks order cancellations as percentage by month.'
) }}

with monthly_statuses as (
    select
        date_trunc('month', order_date)::date as cancellation_month,
        status,
        count(order_id) as order_count
    from {{ ref('fact_orders') }}
    group by date_trunc('month', order_date), status
),

monthly_aggregates as (
    select
        cancellation_month,
        sum(order_count) as total_orders,
        sum(case when status = 'canceled' then order_count else 0 end)
            as cancelled_orders
    from monthly_statuses
    group by cancellation_month
)

select
    cancellation_month,
    total_orders,
    cancelled_orders,
    round(
        case
            when total_orders = 0 then 0
            else (cancelled_orders::numeric / total_orders) * 100
        end,
        2
    ) as cancellation_rate_pct
from monthly_aggregates
order by cancellation_month desc
