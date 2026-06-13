select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select rating
from "ecommerce_db"."public"."raw_reviews"
where rating is null



      
    ) dbt_internal_test