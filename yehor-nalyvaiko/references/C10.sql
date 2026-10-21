-- C10 : commandes passées quand le client avait exactement 25 ans révolus à la date de la commande
-- 25 ans révolus le jour J <=> J-26 ans < naissance <= J-25 ans
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product   p ON p.product_id  = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.birth_date <= date(o.date, '-25 years')
  AND c.birth_date >  date(o.date, '-26 years');
