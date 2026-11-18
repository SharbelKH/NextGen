SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON o.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.product_id = 'd'
  AND o.date >= '2026-09-01 00:00:00'
  AND o.date < '2026-10-01 00:00:00'
  AND c.birth_date = date('2026-09-25', '-25 years');
