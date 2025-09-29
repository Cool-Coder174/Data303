-- Exercise 4.02: Aliasing the Column Headers
-- queries_alias.sql

USE PACKT_ONLINE_SHOP;

-- Select columns with aliases
SELECT ProductCategoryName AS CATEGORY,
       ProductCategoryID   AS ID
FROM ProductCategories;
