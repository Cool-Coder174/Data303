from sqlalchemy import create_engine, text
import csv
import re
from pathlib import Path

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "PACKT_ONLINE_SHOP"

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

with open(Path(__file__).parent / '99_verify.sql', 'r') as f:
    sql_script = f.read()

# Remove comments
sql_script = re.sub(r'--.*\n', '\n', sql_script)

queries = [q.strip() for q in sql_script.split(';') if q.strip()]

with engine.connect() as connection:
    for i, query in enumerate(queries):
        if query.lower().startswith("select"):
            result = connection.execute(text(query))
            rows = result.fetchall()
            with open(f'query_results_{i}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(result.keys())
                writer.writerows(rows)
            print(f"Query results saved to query_results_{i}.csv")
        elif not query.lower().startswith("use "):
            connection.execute(text(query))