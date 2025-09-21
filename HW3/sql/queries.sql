USE employeedemo;

-- Join employee and department to show employee names with department names
SELECT
    e.ename,
    d.dname
FROM
    employee e
JOIN
    department d ON e.deptno = d.dno;

-- Count how many employees are in each department
SELECT
    d.dname,
    COUNT(e.eno) AS num_employees
FROM
    department d
LEFT JOIN
    employee e ON e.deptno = d.dno
GROUP BY
    d.dname;
