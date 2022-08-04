-- Q1: Write an SQL query to print the first three characters of  FIRST_NAME from Worker table.
SELECT SUBSTRING(first_name, 1, 3) FROM worker LIMIT 1;

-- Q2: Write an SQL query to find the position of the alphabet (‘a’) in the first name
--     column ‘Amitabh’ from Worker table.

SELECT POSITION('a' IN 'Amitabh');

-- Q3: Write an SQL query to print the name of employees having the highest salary in each department.
SELECT name, MAX(salary) FROM employees GROUP BY department;