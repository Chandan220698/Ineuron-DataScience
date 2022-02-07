# SQL Assignment - 1

# Q-1. Write an SQL query to fetch “FIRST_NAME” from Worker table using the alias name as <WORKER_NAME>.
select FIRST_NAME as WORKER_NAME from worker;

# Q-2. Write an SQL query to fetch unique values of DEPARTMENT from Worker table.
select distinct DEPARTMENT from WORKER;

# Q-3. Write an SQL query to show the last 5 record from a table.
(select * from WORKER order by FIRST_NAME desc limit 5) ORDER BY FIRST_NAME ASC;