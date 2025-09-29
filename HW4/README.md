# Exercise 4.01 & 4.02: Selecting Columns and Aliasing

This project demonstrates basic SQL SELECT statements and column aliasing using Python to interact with a MySQL database.

## Setup

1.  **MySQL Credentials:**
    Open `main.py` and update the following variables with your MySQL connection details:
    ```python
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "your_password"
    ```

## How to Run

1.  Navigate to the project directory:
    ```bash
    cd HW4
    ```

2.  Run the Python script:
    ```bash
    python3 main.py
    ```

    The script will:
    *   Connect to MySQL.
    *   Create the `PACKT_ONLINE_SHOP` database and `ProductCategories` table.
    *   Insert data into the table.
    *   Run queries and tests.
    *   Save the results into the `results/` directory.

## File Structure

*   `main.py`: The main Python script that orchestrates the database operations.
*   `sql/`:
    *   `schema.sql`: Defines the database and table structure.
    *   `inserts.sql`: Inserts the initial data.
    *   `queries_select.sql`: Contains the query for Exercise 4.01.
    *   `queries_alias.sql`: Contains the query for Exercise 4.02.
    *   `tests/`:
        *   `unit.sql`: Unit tests to verify table structure and data integrity.
        *   `integration.sql`: Integration tests to verify the correctness of the main queries.
*   `results/`:
    *   `output_select.csv`: Output of `queries_select.sql`.
    *   `output_alias.csv`: Output of `queries_alias.sql`.
    *   `unit_test_results.csv`: Results of the unit tests.
    *   `integration_test_results.csv`: Results of the integration tests.
    *   `logs.txt`: Captures any errors that occur during execution.
*   `README.md`: This file.
