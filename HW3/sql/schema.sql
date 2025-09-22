-- Create the database
CREATE DATABASE IF NOT EXISTS employeedemo;
USE employeedemo;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS department;

-- Create the department table
CREATE TABLE department (
    dno INT PRIMARY KEY,
    dname VARCHAR(255),
    dlocation VARCHAR(255)
);

-- Create the employee table
CREATE TABLE employee (
    eno VARCHAR(255) PRIMARY KEY,
    ename VARCHAR(255),
    job VARCHAR(255),
    manager VARCHAR(255),
    jdate DATE,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    salary DECIMAL(10, 2) DEFAULT 0,
    commission DECIMAL(10, 2) DEFAULT 0,
    deptno INT,
    FOREIGN KEY (deptno) REFERENCES department(dno)
);
