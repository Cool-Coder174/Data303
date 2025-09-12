-- Create a simple Employees table for a one-row insert demo
DROP TABLE IF EXISTS Employees;
CREATE TABLE Employees (
  EmployeeID INT PRIMARY KEY,
  FirstName  VARCHAR(50) NOT NULL,
  LastName   VARCHAR(50) NOT NULL,
  Title      VARCHAR(100) NULL,
  HireDate   DATE NULL,
  Salary     DECIMAL(10,2) NULL
);