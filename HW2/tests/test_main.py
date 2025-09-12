
import unittest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import os
import csv
import mysql.connector
import sys

# This is a bit of a hack to import the main.py file
sys.path.append(str(Path(__file__).parent.parent))
import main as main_script

class TestMain(unittest.TestCase):

    def test_split_sql_statements(self):
        # Requirement 8: Safely split SQL on semicolons (don’t split inside quotes).
        self.assertEqual(main_script.split_sql_statements("SELECT * FROM foo;"), ["SELECT * FROM foo"])
        self.assertEqual(main_script.split_sql_statements("SELECT ';'; SELECT \";\";"), ["SELECT ';'", "SELECT \";\""])
        self.assertEqual(main_script.split_sql_statements("SELECT 'a;b'; -- a comment\nSELECT 2;"), ["SELECT 'a;b'", "SELECT 2"])
        self.assertEqual(main_script.split_sql_statements(""), [])
        self.assertEqual(main_script.split_sql_statements("-- a comment"), [])

    @patch('main.export_rows_to_csv')
    def test_run_sql_file(self, mock_export_rows_to_csv):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.with_rows = False
        
        # Create a temporary sql file
        p = Path("test.sql")
        p.write_text("SELECT 1; INSERT INTO foo VALUES (1);")

        main_script.run_sql_file(mock_conn, mock_cursor, p)

        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_cursor.execute.assert_has_calls([call("SELECT 1"), call("INSERT INTO foo VALUES (1)")])
        mock_conn.commit.assert_called_once()
        mock_export_rows_to_csv.assert_not_called()
        
        p.unlink() # clean up

    @patch('main.export_rows_to_csv')
    def test_run_sql_file_with_select(self, mock_export_rows_to_csv):
        mock_export_rows_to_csv.return_value = ("test.csv", 1)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.with_rows = True
        
        p = Path("test_select.sql")
        p.write_text("SELECT * FROM foo;")

        main_script.run_sql_file(mock_conn, mock_cursor, p)

        mock_cursor.execute.assert_called_once_with("SELECT * FROM foo")
        mock_export_rows_to_csv.assert_called_once()
        mock_conn.commit.assert_called_once()

        p.unlink() # clean up

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This will run the main script once before all tests in this class
        # This covers requirements 1, 2, 3, 4, 5
        try:
            main_script.main()
        except Exception as e:
            # If the script fails, we want to know why
            print(f"Running main.py for integration test setup failed: {e}")
            # It's possible the DB doesn't exist, so we can't connect to clean up.
            # We'll have to rely on the error message.
            raise

    @classmethod
    def tearDownClass(cls):
        # Clean up the database after tests
        try:
            conn = main_script.connect_db()
            with conn.cursor() as cur:
                cur.execute("DROP DATABASE IF EXISTS EMPLOYEE;")
            conn.close()
        except mysql.connector.Error as e:
            print(f"Could not clean up database EMPLOYEE: {e}")


    def test_database_and_table_created(self):
        # Requirement 1 & 2: Create an EMPLOYEE database and Employees table.
        conn = main_script.connect_db()
        with conn.cursor() as cur:
            cur.execute("USE EMPLOYEE;")
            cur.execute("SHOW TABLES;")
            tables = [table[0] for table in cur.fetchall()]
            self.assertIn('employees', [t.lower() for t in tables])
        conn.close()

    def test_employee_inserted(self):
        # Requirement 3: Insert one row.
        conn = main_script.connect_db()
        with conn.cursor() as cur:
            cur.execute("USE EMPLOYEE;")
            cur.execute("SELECT COUNT(*) FROM Employees;")
            count = cur.fetchone()[0]
            self.assertEqual(count, 1)

            cur.execute("SELECT * FROM Employees WHERE EmployeeID = 1;")
            employee = cur.fetchone()
            self.assertIsNotNone(employee)
            self.assertEqual(employee[1], 'Grace')
            self.assertEqual(employee[2], 'Hopper')

        conn.close()

    def test_csv_files_created(self):
        # Requirement 5: writes CSVs for any SELECT/SHOW statements into ./output
        output_dir = Path(__file__).parent.parent / "output"
        self.assertTrue((output_dir / "10_select_all_employees.csv").exists())
        self.assertTrue((output_dir / "11_describe_employees.csv").exists())

        # Requirement 6: No pandas; use Python’s built-in csv module.
        # We can verify the content of one of the CSVs
        with open(output_dir / "10_select_all_employees.csv", 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, ['EmployeeID', 'FirstName', 'LastName', 'Title', 'HireDate', 'Salary'])
            row = next(reader)
            self.assertEqual(row[0], '1')
            self.assertEqual(row[1], 'Grace')

if __name__ == '__main__':
    unittest.main()
