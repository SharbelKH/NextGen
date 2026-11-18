-- C05: revenue from 1 June 2026, inclusive, to 2 June 2026, exclusive.
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-06-01 00:00:00'
  AND o.date <  '2026-06-02 00:00:00';

-- C06: revenue from 1 January 2025, inclusive, to 1 January 2026, exclusive.
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2025-01-01 00:00:00'
  AND o.date <  '2026-01-01 00:00:00';