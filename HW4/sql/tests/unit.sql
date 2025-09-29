-- Exercise 4.01 & 4.02: Selecting Columns from a Table & Aliasing the Column Headers
-- unit.sql

USE PACKT_ONLINE_SHOP;

-- Unit tests
SELECT 'table_exists' AS test_name, COUNT(*) AS result FROM information_schema.tables WHERE table_schema = 'PACKT_ONLINE_SHOP' AND table_name = 'ProductCategories'
UNION ALL
SELECT 'row_count' AS test_name, COUNT(*) AS result FROM ProductCategories
UNION ALL
SELECT 'min_id' AS test_name, MIN(ProductCategoryID) AS result FROM ProductCategories
UNION ALL
SELECT 'max_id' AS test_name, MAX(ProductCategoryID) AS result FROM ProductCategories
UNION ALL
SELECT 'distinct_ids' AS test_name, COUNT(DISTINCT ProductCategoryID) AS result FROM ProductCategories
UNION ALL
SELECT 'alias_query_runs' AS test_name, COUNT(*) > 0 AS result FROM (SELECT ProductCategoryName AS CATEGORY, ProductCategoryID AS ID FROM ProductCategories) AS alias_test;
