from pathlib import Path
import sqlite3

folder = Path(__file__).resolve().parent

# Open the database in read-only mode.
database_path = folder / "data" / "boutique.sqlite"
connection = sqlite3.connect(
    database_path.as_uri() + "?mode=ro",
    uri=True,
)

# Read the two queries from the SQL file.
sql_text = (folder / "consultas-c05-c06.sql").read_text(encoding="utf-8")
queries = [query.strip() for query in sql_text.split(";") if query.strip()]

try:
    if len(queries) != 2:
        raise ValueError("Expected exactly two SQL queries: C05 followed by C06.")

    for case_id, query in zip(("C05", "C06"), queries):
        revenue_cents = connection.execute(query).fetchone()[0]
        print(f"{case_id}: revenue_cents = {revenue_cents}")
finally:
    connection.close()