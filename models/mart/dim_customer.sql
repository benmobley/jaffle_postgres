select
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    c.customer_zip_code_prefix
from {{ ref('stg_olist_customers') }} as c
