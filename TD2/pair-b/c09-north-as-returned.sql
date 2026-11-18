-- C09, openrouter:cohere/north-mini-code:free; stored TD1 SQL; logged result: 0 cents.
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE
  -- Compute age on 2026-09-26
  (
    -- Age = year difference
    CAST(SUBSTR(c.birth_date, 1, 4) AS INTEGER) -
    CASE
      WHEN SUBSTR(c.birth_date, 6, 2) > '09' THEN 1
      WHEN SUBSTR(c.birth_date, 6, 2) = '09' AND SUBSTR(c.birth_date, 9, 2) > '26' THEN 1
      ELSE 0
    END
  ) = 25;
