# main.py
# The maestro of this whole symphony. Conducts the SQL scripts in the right order.
# If you mess this up, the whole orchestra goes out of tune.
# Usage:
#   1) Don't just stand there, make sure your .env file has the database credentials.
#      The run.sh script can hold your hand through it if you're scared.
#   2) python main.py -- and pray it works.

import os
import sys
from pathlib import Path
import mysql.connector

def load_env():
    # This function is so basic it's almost embarrassing.
    # It loads the .env file. That's it. Don't expect miracles.
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        # If you don't have python-dotenv installed, this will just... not work.
        # And I'm not going to hold your hand.
        pass

def connect_db():
    # The gateway to our precious data. Or, you know, whatever's in the database.
    # If this fails, the whole script is pointless. No pressure.
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        autocommit=False, # We're not animals. We use transactions.
        connection_timeout=10, # If it takes longer than 10 seconds, it's probably not worth it.
    )

def split_sql_statements(sql: str):
    '''
    Behold, the magic SQL splitter! It dices, it slices, it handles quoted semicolons.
    Why? Because some people like to put multiple commands in one file. Monsters.
    It's simple, but it gets the job done. Unlike some people I know.
    '''
    statements = []
    buf = []
    in_single = False
    in_double = False
    prev = ""
    for ch in sql:
        if ch == "'" and prev != "\\" and not in_double:
            in_single = not in_single
        elif ch == '"' and prev != "\\" and not in_single:
            in_double = not in_double

        if ch == ";" and not in_single and not in_double:
            stmt = "".join(buf).strip()
            if stmt:
                statements.append(stmt)
            buf = []
        else:
            buf.append(ch)
        prev = ch
    tail = "".join(buf).strip()
    if tail:
        statements.append(tail)
    # Get rid of the riff-raff. No empty statements or comments allowed.
    return [s for s in statements if s and not s.lower().startswith("--")]

def run_sql_file(cursor, path: Path):
    # This is where the magic happens. We read a SQL file and run it.
    # Don't blink or you'll miss it.
    print(f"\n-- Running: {path.name}")
    sql = path.read_text(encoding="utf-8")
    stmts = split_sql_statements(sql)
    for i, stmt in enumerate(stmts, 1):
        # A little preview of the action. Because we're considerate like that.
        preview = stmt.strip().split(None, 1)[0].upper() if stmt.strip() else "(empty)"
        print(f"   [{i}/{len(stmts)}] {preview} ...", end="", flush=True)
        cursor.execute(stmt)
        # If there are rows, we have to fetch them. Otherwise, the driver gets cranky.
        if cursor.with_rows:
            _ = cursor.fetchall()
            print(f" ({len(_)} row(s))", end="")
        print(" ✓")
    # And now, for the grand finale... we commit. Or not. Depends on how we feel.
    # Just kidding, we always commit. We're not savages.
    cursor._connection.commit()
    print("   ✓ Committed")

def main():
    # The main event. The big cheese. The whole enchilada.
    load_env()
    sql_dir = Path(__file__).parent / "sql"
    # Let's find all the SQL files and sort them. Because we're organized like that.
    files = sorted(sql_dir.glob("[0-9][0-9]_*.sql"))
    if not files:
        print("No SQL files found in ./sql. Did you delete them? You shouldn't have.")
        sys.exit(1)

    try:
        # Let's try to connect to the database. Fingers crossed.
        conn = connect_db()
    except mysql.connector.Error as e:
        print("MySQL connection error. Did you even start the database? Honestly.", e)
        sys.exit(2)

    try:
        # A cursor is like a little robot that runs our SQL commands. Beep boop.
        with conn.cursor() as cur:
            for f in files:
                run_sql_file(cur, f)
        print("\nAll scripts executed successfully. You're a wizard, Harry. 🚀")
    except mysql.connector.Error as e:
        # If something goes wrong, we roll back the changes. It's like it never even happened.
        conn.rollback()
        print("MySQL execution error. You had one job.", e)
        sys.exit(3)
    finally:
        # Always close the connection. It's just good manners.
        conn.close()

if __name__ == "__main__":
    # If you run this file directly, this is what happens.
    # If you import it, this doesn't run. Magic, right?
    main()