-- Make sure ProductID is AUTO_INCREMENT primary key (PK already exists from HW1)
ALTER TABLE Products
  MODIFY COLUMN ProductID INT NOT NULL AUTO_INCREMENT;