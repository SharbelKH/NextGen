-- C19: list each eligible customer and the revenue omitted by each model.
-- Reference: product d, orders from 2026-09-01 (included) to 2026-10-01 (excluded),
-- customers exactly 25 on 2026-09-25 (born after 2000-09-25, on or before 2001-09-25).
-- Model conditions below reproduce the age predicates of the stored TD1 traces;
-- the product and period filters are identical in both models and in the reference.
WITH classified_orders AS (
    SELECT c.customer_id, c.birth_date, o.date AS order_date,
           o.quantity_product * p.price AS revenue_cents,
           (c.birth_date > '2000-09-25'
            AND c.birth_date <= '2001-09-25') AS reference_match,
           (c.birth_date = date('2026-09-25', '-25 years')) AS gpt120b_match,
           (c.birth_date <= date('2026-09-25', '-' || CAST((strftime('%Y-%m-%d', '2026-09-25') - strftime('%Y-%m-%d', c.birth_date)) / 365 AS INTEGER) || ' years')
            AND c.birth_date > date('2026-09-25', '-' || CAST((strftime('%Y-%m-%d', '2026-09-25') - strftime('%Y-%m-%d', c.birth_date)) / 365 + 1 AS INTEGER) || ' years')) AS north_match
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    JOIN product p ON p.product_id = o.product_id
    WHERE o.product_id = 'd'
      AND o.date >= '2026-09-01 00:00:00'
      AND o.date < '2026-10-01 00:00:00'
)
SELECT customer_id, birth_date,
       SUM(revenue_cents) AS reference_revenue_cents,
       SUM(CASE WHEN NOT gpt120b_match THEN revenue_cents ELSE 0 END)
           AS gpt120b_missed_cents,
       SUM(CASE WHEN NOT north_match THEN revenue_cents ELSE 0 END)
           AS north_missed_cents
FROM classified_orders
WHERE reference_match
GROUP BY customer_id, birth_date
ORDER BY customer_id;
