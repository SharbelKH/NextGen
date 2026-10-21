-- Vérification indépendante de C10 : même formule d'âge révolu, avec la date de chaque commande
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product   p ON p.product_id  = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE (CAST(strftime('%Y', o.date) AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER))
      - (strftime('%m-%d', o.date) < strftime('%m-%d', c.birth_date)) = 25;
