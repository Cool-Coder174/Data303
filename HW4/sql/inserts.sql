-- Exercise 4.01 & 4.02: Selecting Columns from a Table & Aliasing the Column Headers
-- inserts.sql

USE PACKT_ONLINE_SHOP;

-- Insert 7 rows into the ProductCategories table
INSERT INTO ProductCategories (ProductCategoryID, ProductCategoryName) VALUES
(1, 'condiments'),
(2, 'tools'),
(3, 'food'),
(4, 'airships'),
(5, 'software'),
(6, 'books'),
(7, 'horse-drawn carriages');
