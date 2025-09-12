import os
from pathlib import Path
import csv
import mysql.connector

def load_env():
    # Try to load .env file. If python-dotenv is not installed, we'll just carry on.
    # It's like trying to find your keys after a long night out. Maybe they're there, maybe not.
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        # If it fails, we assume the environment variables are set manually.
        # Or maybe they're just living in the ether. Who knows?
        pass

def connect_db():
    # Connect to the database. Or at least, that's the plan.
    # DB_NAME is optional, because we might need to create it first.
    # It's like showing up to a party before it's even started.
    params = dict(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        autocommit=False, # We're not savages. We use transactions.
        connection_timeout=10, # Don't wait forever. Life's too short.
    )
    db = os.getenv("DB_NAME", "").strip()
    if db:
        params["database"] = db
    return mysql.connector.connect(**params)

def split_sql_statements(sql: str):
    """
    Split on semicolons not inside quotes, after removing comments.
    This is trickier than it sounds. It's like trying to split a sandwich perfectly
    without getting any of the filling on your hands.
    """
    # Remove comments first
    sql_no_comments = []
    for line in sql.splitlines():
        sql_no_comments.append(line.split('--')[0].strip())
    sql = " ".join(sql_no_comments)

    stmts, buf = [], []
    in_single = in_double = False
    prev = ""
    for ch in sql:
        # Are we inside a string? Let's check.
        if ch == "'" and prev != '"' and not in_double:
            in_single = not in_single
        elif ch == '"' and prev != '"' and not in_single:
            in_double = not in_double

        # If we're not in a string, a semicolon is a delimiter.
        if ch == ";" and not in_single and not in_double:
            stmt = "".join(buf).strip()
            if stmt:
                stmts.append(stmt)
            buf = []
        else:
            buf.append(ch)
        prev = ch
    # Don't forget the last statement if there's no trailing semicolon.
    # It's the one that always gets left behind.
    tail = "".join(buf).strip()
    if tail:
        stmts.append(tail)
    # And let's get rid of any pesky empty statements.
    return [s for s in stmts if s]

def ensure_dirs():
    # Make sure the output directory exists. If not, create it.
    # It's like making sure you have a plate before you serve yourself dinner.
    (Path(__file__).parent / "output").mkdir(parents=True, exist_ok=True)

def export_rows_to_csv(base_stem: str, result_index: int, cursor):
    # Export query results to a CSV file. Because who doesn't love a good spreadsheet?
    cols = [d[0] for d in cursor.description] # Get the column headers. The boring part.
    rows = cursor.fetchall() # Get the data. The fun part.
    suffix = f"_{result_index}" if result_index > 1 else ""
    out_path = Path(__file__).parent / "output" / f"{base_stem}{suffix}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
    return out_path.name, len(rows)

def run_sql_file(conn, cursor, path: Path):
    # Run a single SQL file. One file to rule them all.
    print(f"\n-- Running: {path.name}")
    sql = path.read_text(encoding="utf-8")
    stmts = split_sql_statements(sql)
    result_index = 0
    for i, stmt in enumerate(stmts, 1):
        first_kw = stmt.strip().split(None, 1)[0].upper() if stmt.strip() else "(empty)"
        print(f"   [{i}/{len(stmts)}] {first_kw} ...", end="", flush=True)
        cursor.execute(stmt)
        # If the statement returned rows, we have work to do.
        if cursor.with_rows:
            result_index += 1
            csv_name, n = export_rows_to_csv(path.stem, result_index, cursor)
            print(f" exported {n} row(s) -> output/{csv_name}")
        else:
            # If not, just a simple checkmark. Easy peasy.
            print(" ✓")
    # Commit the transaction. Make it official.
    conn.commit()
    print("   ✓ Committed")

def main():
    # The main event. The big cheese. The whole enchilada.
    load_env()
    ensure_dirs()
    sql_dir = Path(__file__).parent / "sql"
    files = sorted(sql_dir.glob("[0-9][0-9]_*.sql"))
    if not files:
        print("No SQL files found in ./sql. Are you sure you put them there?")
        return

    conn = connect_db()
    try:
        with conn.cursor() as cur:
            for f in files:
                run_sql_file(conn, cur, f)
        print("\nAll scripts executed successfully. 🚀 Go check your output folder!")
    except mysql.connector.Error as e:
        # If something goes wrong, we roll back. It's like it never even happened.
        conn.rollback()
        print("MySQL execution error:", e)
        raise
    finally:
        # Always close the connection. It's just good manners.
        conn.close()

if __name__ == "__main__":
    # If this script is run directly, call the main function.
    # It's the circle of life.
    main()
