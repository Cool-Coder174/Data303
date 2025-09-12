import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path
import csv

# Import the functions to be tested
from main import (
    split_sql_statements,
    strip_sql_comments,
    ensure_dirs,
    export_rows_to_csv,
    run_sql_file
)

# -- Tests for SQL parsing --

@pytest.mark.parametrize("sql_input, expected_output", [
    # Requirement: Splits SQL safely on semicolons.
    ("SELECT * FROM t1; SELECT * FROM t2;", ["SELECT * FROM t1", "SELECT * FROM t2"]),
    # Requirement: Don’t split inside quotes.
    ("INSERT INTO messages VALUES ('Hello; world');", ["INSERT INTO messages VALUES ('Hello; world')"]),
    ('INSERT INTO messages VALUES ("Hello; world");', ['INSERT INTO messages VALUES ("Hello; world")']),
    # Handles escaped quotes (the bug from before)
    ("INSERT INTO messages VALUES ('Hello \'world\';');", ["INSERT INTO messages VALUES ('Hello \'world\';')"]),
    # Handles no trailing semicolon
    ("SELECT * FROM users", ["SELECT * FROM users"]),
    # Handles multiple semicolons
    (";;SELECT * FROM users;;", ["SELECT * FROM users"]),
    # Handles empty input
    ("", []),
    (";", []),
])
def test_split_sql_statements(sql_input, expected_output):
    """Comprehensive tests for the refactored split_sql_statements."""
    assert split_sql_statements(sql_input) == expected_output

@pytest.mark.parametrize("sql_input, expected_output", [
    # Strips single-line comments
    ("SELECT * FROM users; -- Get all users", "SELECT * FROM users;"),
    # Strips file-leading comments (the other bug)
    ("-- My script\nSELECT * FROM users;", "SELECT * FROM users;"),
    # Strips multi-line comments
    ("/* a comment */ SELECT 1;", "SELECT 1;"),
    ("SELECT /* a comment */ 1;", "SELECT  1;"), # In-line becomes a space
])
def test_strip_sql_comments(sql_input, expected_output):
    """Test the comment stripping logic."""
    assert strip_sql_comments(sql_input) == expected_output

# -- Tests for file system operations --

def test_ensure_dirs(tmp_path: Path):
    """Requirement: It creates the output directory if it doesn't exist."""
    test_output_path = tmp_path / "output"
    assert not test_output_path.exists()
    ensure_dirs(test_output_path)
    assert test_output_path.exists()
    assert test_output_path.is_dir()

def test_export_rows_to_csv(tmp_path: Path):
    """Requirement: Exports SELECT/SHOW results to CSV with headers."""
    # 1. Setup mock cursor
    mock_cursor = Mock()
    mock_cursor.description = [('id',), ('name',)]
    mock_cursor.fetchall.return_value = [ (1, 'Alice'), (2, 'Bob') ]

    # 2. Run the function
    csv_name, num_rows = export_rows_to_csv(
        base_stem="test_export",
        result_index=1,
        cursor=mock_cursor,
        output_path=tmp_path
    )

    # 3. Assertions
    assert num_rows == 2
    assert csv_name == "test_export.csv"
    
    # Check the CSV content
    csv_file = tmp_path / "test_export.csv"
    assert csv_file.exists()
    with csv_file.open('r', newline='') as f:
        reader = csv.reader(f)
        assert next(reader) == ['id', 'name']
        assert next(reader) == ['1', 'Alice']
        assert next(reader) == ['2', 'Bob']

def test_run_sql_file(tmp_path: Path, capsys):
    """Requirement: Runs every .sql file and commits after each."""
    # 1. Create a fake SQL file
    sql_content = "-- A test query\nSELECT * FROM test_table;\nINSERT INTO audit_log VALUES ('ran test');"
    sql_file = tmp_path / "01_test.sql"
    sql_file.write_text(sql_content)

    # 2. Setup mock cursor and connection
    mock_cursor = MagicMock()
    mock_cursor.with_rows = False # Default for INSERT
    mock_conn = Mock()
    mock_cursor.connection = mock_conn

    # 3. Run the function
    run_sql_file(mock_cursor, sql_file, output_path=tmp_path)

    # 4. Assertions
    # Check that execute was called for each statement
    assert mock_cursor.execute.call_count == 2
    mock_cursor.execute.assert_any_call("SELECT * FROM test_table")
    mock_cursor.execute.assert_any_call("INSERT INTO audit_log VALUES ('ran test')")

    # Check that commit was called
    mock_conn.commit.assert_called_once()

    # Check console output
    captured = capsys.readouterr()
    assert "-- Running: 01_test.sql" in captured.out
    assert "[1/2] SELECT ... ✓" in captured.out
    assert "[2/2] INSERT ... ✓" in captured.out
    assert "✓ Committed" in captured.out