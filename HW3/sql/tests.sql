USE employeedemo;

-- Confirm all 4 departments exist
SELECT COUNT(*) AS num_departments FROM department;

-- Confirm all 4 employees are inserted correctly
SELECT COUNT(*) AS num_employees FROM employee;

-- Confirm no employee references an invalid department
SELECT
    e.eno,
    e.ename,
    e.deptno
FROM
    employee e
WHERE
    e.deptno NOT IN (SELECT dno FROM department);
