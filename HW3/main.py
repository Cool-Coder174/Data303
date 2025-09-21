import mysql.connector
import os

def execute_sql_from_file(filename, cursor):
    with open(filename, 'r') as f:
        sql_script = f.read()
    # Split script into individual statements
    sql_statements = sql_script.split(';')
    for statement in sql_statements:
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print(f"Error executing statement: {statement}\n{e}")

def main():
    # Connect to MySQL server
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return

    cursor = conn.cursor()

    # Create and select the database
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS employeedemo")
        cursor.execute("USE employeedemo")
    except mysql.connector.Error as e:
        print(f"Error creating or selecting database: {e}")
        conn.close()
        return

    # Create output directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    output_file = 'results/output.txt'

    with open(output_file, 'w') as f:
        f.write("Homework 3 Output\n")
        f.write("="*20 + "\n\n")

        # Execute schema.sql
        f.write("Executing schema.sql...\n")
        execute_sql_from_file('sql/schema.sql', cursor)
        f.write("schema.sql executed successfully.\n\n")

        # Execute inserts.sql
        f.write("Executing inserts.sql...\n")
        execute_sql_from_file('sql/inserts.sql', cursor)
        f.write("inserts.sql executed successfully.\n\n")

        # Execute queries.sql and write output
        f.write("Executing queries.sql...\n")
        with open('sql/queries.sql', 'r') as queries_f:
            queries_sql = queries_f.read()
        queries = queries_sql.split(';')
        for query in queries:
            if query.strip():
                f.write(f"Query: {query.strip()}\n")
                try:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    if results:
                        for row in results:
                            f.write(str(row) + '\n')
                    else:
                        f.write("No results.\n")
                except mysql.connector.Error as e:
                    f.write(f"Error executing query: {e}\n")
                f.write("-" * 20 + "\n")
        f.write("queries.sql executed successfully.\n\n")

        # Execute tests.sql and write output
        f.write("Executing tests.sql...\n")
        with open('sql/tests.sql', 'r') as tests_f:
            tests_sql = tests_f.read()
        tests = tests_sql.split(';')
        for test in tests:
            if test.strip():
                f.write(f"Test: {test.strip()}\n")
                try:
                    cursor.execute(test)
                    results = cursor.fetchall()
                    if results:
                        for row in results:
                            f.write(str(row) + '\n')
                    else:
                        f.write("No results.\n")
                except mysql.connector.Error as e:
                    f.write(f"Error executing test: {e}\n")
                f.write("-" * 20 + "\n")
        f.write("tests.sql executed successfully.\n\n")

    conn.commit()
    conn.close()

    print(f"Script executed successfully. Output written to {output_file}")

if __name__ == '__main__':
    main()