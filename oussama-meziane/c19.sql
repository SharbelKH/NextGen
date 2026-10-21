SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON p.product_id = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.product_id = 'd'
  AND o.date >= '2026-09-01 00:00:00'
  AND o.date < '2026-10-01 00:00:00'
  AND (CAST(strftime('%Y', '2026-09-25') AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER))
      - (strftime('%m-%d', '2026-09-25') < strftime('%m-%d', c.birth_date)) = 25;