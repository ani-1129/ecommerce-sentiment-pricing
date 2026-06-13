select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select shipping_city
from "ecommerce_db"."public"."raw_orders"
where shipping_city is null



      
    ) dbt_internal_test