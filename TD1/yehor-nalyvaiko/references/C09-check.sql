-- C09 check: year difference, minus 1 if birthday not reached yet
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product   p ON p.product_id  = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE (2026 - CAST(strftime('%Y', c.birth_date) AS INTEGER))
      - ('09-26' < strftime('%m-%d', c.birth_date)) = 25;
