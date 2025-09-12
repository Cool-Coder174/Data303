-- Show only the three Activity 2.01 products
SELECT ProductID, ProductName, NetRetailPrice, WholesalePrice, ProductCategoryID
FROM Products
WHERE ProductName IN ('Pancake batter', 'Breakfast cereal', 'Siracha sauce')
ORDER BY ProductID;