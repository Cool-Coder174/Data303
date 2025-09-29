
import mysql.connector
import csv
import os

# --- DATABASE CREDENTIALS ---
# Replace with your MySQL connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "PACKT_ONLINE_SHOP"

# --- FILE PATHS ---
SQL_DIR = "sql"
RESULTS_DIR = "results"
LOG_FILE = os.path.join(RESULTS_DIR, "logs.txt")

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

def execute_sql_from_file(cursor, file_path):
    """Reads and executes SQL statements from a file."""
    with open(file_path, 'r') as f:
        # Split statements by semicolon and filter out empty ones
        statements = [s.strip() for s in f.read().split(';') if s.strip()]
        for statement in statements:
            try:
                cursor.execute(statement)
            except mysql.connector.Error as err:
                with open(LOG_FILE, 'a') as log:
                    log.write(f"Error executing statement from {file_path}: {statement}\n")
                    log.write(f"MySQL Error: {err}\n")
                raise

def fetch_and_write_csv(cursor, query, file_path):
    """Executes a query, fetches all results, and writes to a CSV file."""
    try:
        statements = [s.strip() for s in query.split(';') if s.strip()]
        for statement in statements:
            cursor.execute(statement)
        
        headers = [i[0] for i in cursor.description]
        rows = cursor.fetchall()

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(rows)
    except mysql.connector.Error as err:
        with open(LOG_FILE, 'a') as log:
            log.write(f"Error fetching or writing CSV for query: {query}\n")
            log.write(f"MySQL Error: {err}\n")
        raise

def main():
    """Main script execution."""
    # Clear log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    try:
        # Connect to MySQL server (without specifying a database initially)
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = cnx.cursor()

        # --- DATABASE AND TABLE SETUP ---
        execute_sql_from_file(cursor, os.path.join(SQL_DIR, "schema.sql"))
        
        # Now connect to the specific database
        cnx.database = DB_DATABASE
        
        execute_sql_from_file(cursor, os.path.join(SQL_DIR, "inserts.sql"))

        # --- RUN QUERIES AND SAVE RESULTS ---
        with open(os.path.join(SQL_DIR, "queries_select.sql"), 'r') as f:
            query_select = f.read()
        fetch_and_write_csv(cursor, query_select, os.path.join(RESULTS_DIR, "output_select.csv"))

        with open(os.path.join(SQL_DIR, "queries_alias.sql"), 'r') as f:
            query_alias = f.read()
        fetch_and_write_csv(cursor, query_alias, os.path.join(RESULTS_DIR, "output_alias.csv"))

        # --- RUN TESTS AND SAVE RESULTS ---
        with open(os.path.join(SQL_DIR, "tests", "unit.sql"), 'r') as f:
            unit_tests_query = f.read()
        fetch_and_write_csv(cursor, unit_tests_query, os.path.join(RESULTS_DIR, "unit_test_results.csv"))

        with open(os.path.join(SQL_DIR, "tests", "integration.sql"), 'r') as f:
            integration_tests_query = f.read()
        fetch_and_write_csv(cursor, integration_tests_query, os.path.join(RESULTS_DIR, "integration_test_results.csv"))

        print("Script completed successfully.")

    except mysql.connector.Error as err:
        print(f"A MySQL error occurred: {err}")
        print(f"Check {LOG_FILE} for details.")

    finally:
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()

if __name__ == "__main__":
    main()
