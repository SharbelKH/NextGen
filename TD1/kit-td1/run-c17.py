from pathlib import Path
import sqlite3

folder = Path(__file__).resolve().parent
database_path = folder / "data" / "boutique.sqlite"
query = (folder / "query-c17.sql").read_text(encoding="utf-8")

# Open the database in read-only mode and execute the query.
with sqlite3.connect(database_path.as_uri() + "?mode=ro", uri=True) as connection:
    revenue_cents = connection.execute(query).fetchone()[0]
    print(f"C17: revenue_cents = {revenue_cents}")