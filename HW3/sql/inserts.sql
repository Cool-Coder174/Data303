USE employeedemo;

-- Insert data into the department table
INSERT INTO department (dno, dname, dlocation) VALUES
(1, 'HR', 'New York'),
(2, 'Finance', 'Chicago'),
(3, 'IT', 'San Jose'),
(4, 'Marketing', 'Dallas');

-- Insert data into the employee table
INSERT INTO employee (eno, ename, job, manager, jdate, gender, salary, commission, deptno) VALUES
('E101', 'John Doe', 'Analyst', NULL, '2020-01-01', 'M', 60000, 5000, 2),
('E102', 'Jane Roe', 'Manager', 'E101', '2019-05-12', 'F', 80000, 7000, 1),
('E103', 'Alan S', 'Developer', 'E102', '2021-03-15', 'M', 75000, 3000, 3),
('E104', 'Maria L', 'Sales Rep', 'E102', '2022-07-21', 'F', 55000, 4000, 4);
