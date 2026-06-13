select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select verified_purchase
from "ecommerce_db"."public"."raw_reviews"
where verified_purchase is null



      
    ) dbt_internal_test