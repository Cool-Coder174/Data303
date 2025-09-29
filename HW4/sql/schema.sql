-- Exercise 4.01 & 4.02: Selecting Columns from a Table & Aliasing the Column Headers
-- schema.sql

-- Database setup
CREATE DATABASE IF NOT EXISTS PACKT_ONLINE_SHOP;
USE PACKT_ONLINE_SHOP;

-- Drop the table if it exists
DROP TABLE IF EXISTS ProductCategories;

-- Create the table
CREATE TABLE ProductCategories (
    ProductCategoryID INT PRIMARY KEY,
    ProductCategoryName VARCHAR(100) NOT NULL
);
