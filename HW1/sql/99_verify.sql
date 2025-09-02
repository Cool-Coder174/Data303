-- Last but not least, let's verify that we actually did something.
USE PACKT_ONLINE_SHOP;

-- How many customers do we have? Are they even real?
SELECT COUNT(*) AS customers_count FROM Customers;
-- How many products do we have? Are they any good?
SELECT COUNT(*) AS products_count  FROM Products;

-- Let's see some of these so-called "customers".
SELECT FirstName, LastName, Phone FROM Customers LIMIT 10;
-- And the "products".
SELECT ProductID, ProductName, NetRetailPrice, AvailableQuantity
FROM Products
ORDER BY ProductID
LIMIT 10;