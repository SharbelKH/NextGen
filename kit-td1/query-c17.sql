-- C17: revenue from products a, b and c between 1 January 2026
-- (inclusive) and 1 July 2026 (exclusive), for customers aged
-- exactly 25 on 25 September 2026.
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.product_id IN ('a', 'b', 'c')
  AND o.date >= '2026-01-01 00:00:00'
  AND o.date <  '2026-07-01 00:00:00'
  AND c.birth_date >  '2000-09-25'
  AND c.birth_date <= '2001-09-25';