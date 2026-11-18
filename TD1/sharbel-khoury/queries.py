import sqlite3
from pathlib import Path

# Locate the shared database regardless of the terminal's working directory.
database = Path(__file__).resolve().parents[1] / "kit-td1" / "data" / "boutique.sqlite"

connection = sqlite3.connect(
    database.as_uri() + "?mode=ro",
    uri=True
)

query = "SELECT * FROM product;"

query15 = """
SELECT
    COALESCE(
        SUM(o.quantity_product * p.price),
        0
    ) AS revenue_cents
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
JOIN product AS p
    ON o.product_id = p.product_id
WHERE o.date >= '2026-03-01 00:00:00'
  AND o.date <  '2026-06-01 00:00:00'
  AND c.birth_date >  '2000-09-25'
  AND c.birth_date <= '2001-09-25';
"""

query16 = """
SELECT
    COALESCE(
        SUM(o.quantity_product * p.price),
        0
    ) AS revenue_cents
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
JOIN product AS p
    ON o.product_id = p.product_id
WHERE c.birth_date >  '2000-09-25'
  AND c.birth_date <= '2001-09-25'
  AND p.product_id IN ('a', 'b', 'c');
"""

rows = connection.execute(query16).fetchall()

for row in rows:
    print(row)

connection.close()
