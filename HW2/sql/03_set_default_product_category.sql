-- Ensure ProductCategoryID defaults to 1 (robust MODIFY syntax)
ALTER TABLE Products
  MODIFY COLUMN ProductCategoryID INT NOT NULL DEFAULT 1;