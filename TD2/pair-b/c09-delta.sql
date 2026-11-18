-- C09: list each eligible customer and the revenue omitted by each model.
-- Reference: exactly 25 on 2026-09-26, across ALL orders.
-- Model conditions below reproduce the WHERE clauses in the stored TD1 traces.
WITH classified_orders AS (
    SELECT c.customer_id, c.birth_date, o.date AS order_date,
           o.quantity_product * p.price AS revenue_cents,
           (c.birth_date > '2000-09-26'
            AND c.birth_date <= '2001-09-26') AS reference_match,
           ((CAST(SUBSTR(c.birth_date, 1, 4) AS INTEGER) -
             CASE
               WHEN SUBSTR(c.birth_date, 6, 2) > '09' THEN 1
               WHEN SUBSTR(c.birth_date, 6, 2) = '09'
                    AND SUBSTR(c.birth_date, 9, 2) > '26' THEN 1
               ELSE 0
             END) = 25) AS north_match,
           ((strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
             AND strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date)
             AND strftime('%m-%d', o.date) <
                 strftime('%m-%d', date(c.birth_date, '+26 years'))) AS qwen_match
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    JOIN product p ON p.product_id = o.product_id
)
SELECT customer_id, birth_date,
       SUM(revenue_cents) AS reference_revenue_cents,
       SUM(CASE WHEN NOT north_match THEN revenue_cents ELSE 0 END)
           AS north_missed_cents,
       SUM(CASE WHEN NOT qwen_match THEN revenue_cents ELSE 0 END)
           AS qwen_missed_cents
FROM classified_orders
WHERE reference_match
GROUP BY customer_id, birth_date
HAVING north_missed_cents <> 0 OR qwen_missed_cents <> 0
ORDER BY customer_id;
