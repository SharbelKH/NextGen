-- C09 : clients ayant exactement 25 ans révolus le 2026-09-26 (toutes leurs commandes)
-- 25 ans révolus le 2026-09-26 <=> né après le 2000-09-26 et au plus tard le 2001-09-26
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product   p ON p.product_id  = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.birth_date > '2000-09-26'
  AND c.birth_date <= '2001-09-26';
