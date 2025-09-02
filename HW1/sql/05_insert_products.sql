-- You guessed it. We're in the PACKT_ONLINE_SHOP database.
USE PACKT_ONLINE_SHOP;

-- Let's add some products. These are also totally real.
INSERT INTO Products
  (ProductID, ProductCategoryID, SupplierID, ProductName,
   NetRetailPrice, AvailableQuantity, WholesalePrice, UnitKGWeight, Notes)
VALUES
  (1, 5, 2, 'Calculatre',             24.99, 100, 17.99, 1,     'It calculates. What more do you want?'),
  (2, 5, 5, 'Penwrite',               79.99,  27, 49.99, 2,     'It writes. With a pen. Get it?'),
  (3, 1, 6, 'Vortex Generator',     2499.99,1000,1999.99,0.01,  'Generates vortexes. Obviously.'),
  (4, 1, 6, 'The Gourmet Crockpot',   24.99,  72, 19.99, 1.63,  'For when you want to pretend you can cook.'),
  (5, 1, 6, 'Account Books',          14.99,  26,  9.99, 1.22,  'For all your... accounting needs.'),
  (6, 3, 6, 'habanero peppers',        4.49, 189,  2.99, 0.009, 'Warning: may cause spontaneous combustion.'),
  (7, 2, 1, '10-mm socket wrench',     3.49,  39,  1.89, 0.018, 'Good luck finding it when you need it.');