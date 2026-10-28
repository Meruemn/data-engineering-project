
-- 1. Overall transaction summary
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM public.transactions;


-- 2. Transaction summary by status
SELECT
    status,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM public.transactions
GROUP BY status
ORDER BY total_amount DESC;


-- 3. Completed transactions by value category
SELECT
    CASE
        WHEN amount >= 3000 THEN 'High Value'
        WHEN amount >= 1000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS transaction_category,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount
FROM public.transactions
WHERE status = 'COMPLETED'
GROUP BY transaction_category
ORDER BY total_amount DESC;


-- 4. High-value completed transactions
SELECT
    transaction_id,
    customer_id,
    transaction_date,
    amount,
    currency
FROM public.transactions
WHERE status = 'COMPLETED'
  AND amount > 2000
ORDER BY amount DESC;
