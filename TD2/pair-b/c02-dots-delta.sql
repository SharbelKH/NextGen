
SELECT
    c.customer_id,
    c.birth_date,
    o.date AS order_date,
    SUM(o.quantity_product * p.price) AS omitted_revenue_cents
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN product AS p ON p.product_id = o.product_id
WHERE c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25'
  AND NOT (
      c.birth_date = '2001-09-25'
      AND o.date >= '2026-09-25 00:00:00'
      AND o.date < '2026-09-26 00:00:00'
  )
GROUP BY c.customer_id, c.birth_date, o.date
ORDER BY c.customer_id, o.date;
