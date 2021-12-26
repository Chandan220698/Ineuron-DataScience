show databases;

create database test1_sql;
show databases;

-- DATABASE test1_py and test_table created using py
use test1_py;
select * from test_table;  -- No data inside test_table as of now
-- Inserted a data using py
select * from test_table; -- Still no data showing
-- Done the commit()
select * from test_table;  -- Now data is showing
-- Inserted 3 more values
select * from test_table;

select * from test1_py.mydata_table;

select * from test1_py.GlassData;
select * from test1_py.GlassData1;
