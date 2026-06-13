-- Raw Orders Landing Zone (No transformation - just copy from source)
SELECT
    order_id,
    customer_id,
    product_id,
    quantity,
    price,
    order_status,
    order_date,
    shipping_city,
    loaded_at
FROM {{ source('raw', 'raw_orders') }}