# Observations

## What did you learn?

I learned how to use Python's `mysql.connector` library to interact with a MySQL database. I also learned how to create a database schema, insert data, and run queries and tests from a Python script. This exercise was a good review of basic SQL commands and how to use them in a real-world scenario.

## Challenges encountered

One challenge I encountered was connecting to the MySQL server. I had to make sure the MySQL server was running and that I had the correct credentials (username and password) to connect to it. I also had to make sure the `mysql-connector-python` library was installed.

Another challenge was that the `mysql.connector` library in Python does not support multiple statements in a single `execute()` call by default. I had to split the SQL scripts into individual statements and execute them one by one.

## How they were solved

I solved the first challenge by starting the MySQL server and providing the correct credentials in the `main.py` file. I also installed the `mysql-connector-python` library using pip.

I solved the second challenge by splitting the SQL scripts into individual statements using the `split(';')` method. I then iterated over the statements and executed them one by one.