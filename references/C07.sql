SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON o.product_id = p.product_id
WHERE o.date >= '2026-05-31 00:00:00'
  AND o.date <  '2026-06-01 00:00:00';
