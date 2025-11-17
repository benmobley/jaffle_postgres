with payments as (
    select
        order_id,
        sum(payment_value) as total_amount
    from {{ ref('stg_olist_payments') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_purchase_ts as order_date,
    o.order_status as status,
    coalesce(p.total_amount, 0) as total_amount
from {{ ref('stg_olist_orders') }} as o
left join payments as p on o.order_id = p.order_id
