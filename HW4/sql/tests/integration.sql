-- Exercise 4.01 & 4.02: Selecting Columns from a Table & Aliasing the Column Headers
-- integration.sql

USE PACKT_ONLINE_SHOP;

-- Integration tests
SELECT 'select_row_count' AS test_name, COUNT(*) AS result FROM (SELECT ProductCategoryID, ProductCategoryName FROM ProductCategories) AS select_test
UNION ALL
SELECT 'alias_row_count' AS test_name, COUNT(*) AS result FROM (SELECT ProductCategoryName AS CATEGORY, ProductCategoryID AS ID FROM ProductCategories) AS alias_test
UNION ALL
SELECT 'row_counts_match' AS test_name, (SELECT COUNT(*) FROM ProductCategories) = (SELECT COUNT(*) FROM (SELECT ProductCategoryName AS CATEGORY, ProductCategoryID AS ID FROM ProductCategories) AS alias_test) AS result;
