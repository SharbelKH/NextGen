SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date >  date('2026-09-24', '-26 years')
  AND c.birth_date <= date('2026-09-24', '-25 years');
