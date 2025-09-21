# Observations

## What did you learn?

I learned how to use Python's `sqlite3` library to interact with a SQLite database. I also learned how to create a database schema, insert data, and run queries and tests from a Python script. This exercise was a good review of basic SQL commands and how to use them in a real-world scenario.

## Challenges encountered

One challenge I encountered was with the `CREATE DATABASE` command. In SQLite, you don't need to explicitly create a database file before connecting to it. The `sqlite3.connect()` function will create the database file if it doesn't exist. I had to modify the `schema.sql` file to remove the `CREATE DATABASE` and `USE` statements, as they are not supported by SQLite.

Another challenge was that the `sqlite3` library in Python does not support multiple statements in a single `execute()` call. I had to split the SQL scripts into individual statements and execute them one by one.

## How they were solved

I solved the first challenge by removing the `CREATE DATABASE` and `USE` statements from the `schema.sql` file. I also modified the `main.py` file to delete the database file if it already exists, so that the script can be run multiple times without errors.

I solved the second challenge by splitting the SQL scripts into individual statements using the `split(';')` method. I then iterated over the statements and executed them one by one.
