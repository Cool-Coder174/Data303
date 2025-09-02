




'''
This script executes SQL queries from a file and outputs the results to a CSV file.
'''

import csv
import mysql.connector
from mysql.connector import Error
import re
from pathlib import Path

# --- DATABASE CONNECTION DETAILS ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""

def run_sql_from_file(filename):
    '''
    Reads SQL queries from a file, executes them, and saves the results to CSV files.
    '''
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        if conn.is_connected():
            print(f"Successfully connected to database")
            print("-" * 30)

            with open(filename, 'r') as f:
                sql_script = f.read()

            # Remove comments
            sql_script = re.sub(r'--.*\n', '\n', sql_script)

            queries = [q.strip() for q in sql_script.split(';') if q.strip()]

            for i, query in enumerate(queries):
                if not query:
                    continue

                print(f"Executing query:\n{query}\n")
                if query.lower().startswith("use "):
                    try:
                        db_name = query.split()[1].replace(';', '')
                        conn.database = db_name
                        print(f"Database changed to {db_name}")
                    except Exception as e:
                        print(f"Error executing USE query: {e}")
                elif query.lower().startswith("select"):
                    try:
                        cursor = conn.cursor()
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        with open(f'query_results_sql_{i}.csv', 'w', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([i[0] for i in cursor.description])
                            writer.writerows(rows)
                        print(f"Query results saved to query_results_sql_{i}.csv")
                        cursor.close()
                    except Exception as e:
                        print(f"Error executing SELECT query: {e}")
                else:
                    try:
                        cursor = conn.cursor()
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        print("Query executed successfully.")
                    except Exception as e:
                        print(f"Error executing non-SELECT query: {e}")
                print("-" * 30)

    except Error as e:
        print(f"Error connecting to MySQL database: {e}")

    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    run_sql_from_file(Path(__file__).parent / '99_verify.sql')




