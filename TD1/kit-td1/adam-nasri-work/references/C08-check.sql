SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE CAST((strftime('%Y%m%d', '2026-09-24') - strftime('%Y%m%d', c.birth_date)) / 10000 AS INT) = 25;
