
  
    

  create  table "ecommerce_db"."public"."raw_orders__dbt_tmp"
  
  
    as
  
  (
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
FROM "ecommerce_db"."public"."raw_orders"
  );
  