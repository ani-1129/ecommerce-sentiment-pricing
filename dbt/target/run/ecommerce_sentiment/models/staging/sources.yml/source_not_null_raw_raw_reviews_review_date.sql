select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select review_date
from "ecommerce_db"."public"."raw_reviews"
where review_date is null



      
    ) dbt_internal_test