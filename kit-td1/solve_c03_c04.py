import sqlite3

conn = sqlite3.connect("data/boutique.sqlite")
cursor = conn.cursor()

# Question C03
sql_c03 = """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON o.product_id = p.product_id
WHERE o.product_id IN ('a', 'b', 'c')
AND o.date >= '2026-01-01 00:00:00'
AND o.date < '2026-07-01 00:00:00'
"""

# Question C04
sql_c04 = """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON o.product_id = p.product_id
WHERE o.date >= '2026-01-01 00:00:00'
AND o.date < '2026-10-01 00:00:00'
"""

cursor.execute(sql_c03)
result_c03 = cursor.fetchone()[0]

cursor.execute(sql_c04)
result_c04 = cursor.fetchone()[0]

print("C03:", result_c03, "cents")
print("C03 correct:", result_c03 == 936350)

print("C04:", result_c04, "cents")
print("C04 correct:", result_c04 == 2826250)

conn.close()