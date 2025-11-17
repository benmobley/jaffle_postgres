{{ config(
    materialized='table',
    description='Top customers by total spend. Rankings based on cumulative order amounts.'
) }}

with customer_spending as (
    select
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        sum(o.total_amount) as total_spend,
        count(distinct o.order_id) as order_count,
        row_number() over (order by sum(o.total_amount) desc) as spend_rank
    from {{ ref('dim_customer') }} as c
    left join {{ ref('fact_orders') }} as o on c.customer_id = o.customer_id
    group by c.customer_id, c.first_name, c.last_name, c.email
)

select
    customer_id,
    first_name,
    last_name,
    email,
    order_count,
    spend_rank,
    round(total_spend, 2) as total_spend
from customer_spending
where total_spend > 0
order by spend_rank
