-- Question 13
SELECT sum(o.quantity_product*p.price) as total_revenue 
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
WHERE o.product_id IN ('a','c')
AND o.date >= '2026-04-01 00:00:00'
AND o.date <= '2026-05-01 00:00:00'


-- Question 14
SELECT sum(o.quantity_product*p.price) as total_revenue
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
WHERE o.product_id IN ('a','b','c')
AND o.date >= '2026-10-01 00:00:00'
AND o.date <= '2026-12-01 00:00:00'

-- Question 18
SELECT SUM(o.quantity_product * p.price) AS total_revenue
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE o.date >= '2026-05-01'
  AND o.date <  '2026-06-01'
  AND CAST(strftime('%Y', o.date) AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)
      - (strftime('%m-%d', o.date) < strftime('%m-%d', c.birth_date)) = 25

-- Question 19
SELECT SUM(o.quantity_product * p.price) AS total_revenue
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE o.product_id = 'd'
  AND o.date >= '2026-09-01'
  AND o.date <  '2026-12-01'
  AND c.birth_date >  '2000-09-25'
  AND c.birth_date <= '2001-09-25';

-- Question 20
SELECT sum(o.quantity_product*p.price) as total_revenue 
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
WHERE o.date >= '2026-06-01 00:00:00'
AND o.date <= '2026-09-01 00:00:00'