import os
from pathlib import Path
import csv
import re
import mysql.connector
from mysql.connector import errorcode

# --- Constants ---
ROOT_PATH = Path(__file__).parent
OUTPUT_PATH = ROOT_PATH / "output"
SQL_PATH = ROOT_PATH / "sql"

def load_env():
    """Load .env file if it exists, but don't cry if it doesn't."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # If python-dotenv isn't around, we just rely on the actual environment.
        pass

def connect_db():
    """Connect to the database using credentials from environment variables."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", ""),
            autocommit=False,
            connection_timeout=10,
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise

def strip_sql_comments(sql: str) -> str:
    """Remove SQL comments. Simple, not 100% foolproof, but good enough for us."""
    sql = re.sub(r"--.*", "", sql)  # Strip single-line comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL) # Strip multi-line comments
    return sql.strip()

def split_sql_statements(sql: str):
    """
    Split on semicolons that aren't inside quotes.
    This is a bit more robust now.
    """
    # First, let's get rid of comments, they just complicate things.
    sql = strip_sql_comments(sql)

    stmts, buf = [], []
    in_single = in_double = False
    prev_ch = ""

    for ch in sql:
        if ch == "'" and prev_ch != '\\' and not in_double:
            in_single = not in_single
        elif ch == '"' and prev_ch != '\\' and not in_single:
            in_double = not in_double

        if ch == ";" and not in_single and not in_double:
            stmt = "".join(buf).strip()
            if stmt:
                stmts.append(stmt)
            buf = []
        else:
            buf.append(ch)
        prev_ch = ch

    tail = "".join(buf).strip()
    if tail:
        stmts.append(tail)

    return [s for s in stmts if s]

def ensure_dirs(path: Path = OUTPUT_PATH):
    """Make sure the output directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def export_rows_to_csv(base_stem: str, result_index: int, cursor, output_path: Path = OUTPUT_PATH):
    """You've got rows, we've got a CSV writer. Let's do this."""
    cols = [d[0] for d in cursor.description]
    rows = cursor.fetchall()
    suffix = f"_{result_index}" if result_index > 1 else ""
    out_file = output_path / f"{base_stem}{suffix}.csv"

    with out_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
    return out_file.name, len(rows)

def run_sql_file(cursor, path: Path, output_path: Path = OUTPUT_PATH):
    """Run a single SQL file, statement by statement."""
    print(f"\n-- Running: {path.name}")
    sql = path.read_text(encoding="utf-8")
    stmts = split_sql_statements(sql)
    result_index = 0

    if not stmts:
        print("   No executable statements found.")
        return

    for i, stmt in enumerate(stmts, 1):
        first_kw = stmt.strip().split(None, 1)[0].upper() if stmt.strip() else "(empty)"
        print(f"   [{i}/{len(stmts)}] {first_kw} ...", end="", flush=True)
        cursor.execute(stmt)
        if cursor.with_rows:
            result_index += 1
            csv_name, n = export_rows_to_csv(path.stem, result_index, cursor, output_path=output_path)
            print(f" exported {n} row(s) -> {output_path.name}/{csv_name}")
        else:
            print(" ✓")
    cursor.connection.commit()
    print("   ✓ Committed")

def main():
    """The main event. Let's get this party started."""
    load_env()
    ensure_dirs()

    sql_files = sorted(SQL_PATH.glob("[0-9][0-9]_*.sql"))
    if not sql_files:
        print(f"No SQL files found in {SQL_PATH}")
        return

    try:
        conn = connect_db()
        with conn.cursor() as cur:
            for f in sql_files:
                run_sql_file(cur, f)
        print("\nAll scripts executed successfully. 🚀")
    except mysql.connector.Error as e:
        print(f"\nMySQL execution error: {e}")
        # No rollback needed, autocommit is False and we commit per file.
        # The connection context manager will handle closing.
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()