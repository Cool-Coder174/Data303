-- Once more, into the breach! We're in the PACKT_ONLINE_SHOP database.
USE PACKT_ONLINE_SHOP;

-- If the Products table exists, it's toast.
DROP TABLE IF EXISTS Products;
-- Now, let's create the Products table. This is where we keep all the stuff we sell.
CREATE TABLE Products (
  ProductID          INT NOT NULL, -- Every product needs a unique ID. It's like a social security number for things.
  ProductCategoryID  INT NOT NULL, -- What kind of thing is it? A book? A gadget? A mystery box?
  SupplierID         INT NOT NULL, -- Who do we get it from?
  ProductName        CHAR(50) NOT NULL, -- What's it called?
  NetRetailPrice     DECIMAL(10,2) NULL, -- How much we sell it for. The NULL means we can be indecisive.
  AvailableQuantity  INT NOT NULL, -- How many we have in stock.
  WholesalePrice     DECIMAL(10,2) NOT NULL, -- How much we paid for it. Don't tell the customers.
  UnitKGWeight       DECIMAL(10,5) NULL, -- How heavy it is. For shipping calculations and whatnot.
  Notes              VARCHAR(750) NULL, -- More juicy gossip.
  PRIMARY KEY (ProductID) -- This makes sure every ProductID is unique. No duplicates allowed.
);