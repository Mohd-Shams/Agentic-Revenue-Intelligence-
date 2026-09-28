-- 1. Regional Profit Decline — CTE + Window Function

-- Question:
-- Which region had the largest decline in profit from Q3 to Q4, and what were its Q3 profit, Q4 profit, and percentage decline?

WITH Q3 AS(SELECT region , ROUND(SUM(profit)) AS Q3_PROFIT 
FROM ecommerce_cleaned
GROUP BY region,quarter
HAVING quarter = 3),

Q4 AS(SELECT region , ROUND(SUM(profit)) AS Q4_PROFIT 
FROM ecommerce_cleaned
GROUP BY region,quarter
HAVING quarter = 4),

 merge AS (SELECT 
	A.region,
    A.Q3_PROFIT ,
    B.Q4_PROFIT 
    
FROM Q3 A
JOIN Q4 B
    ON A.region= B.region)

SELECT region, Q3_PROFIT,Q4_PROFIT, (Q3_PROFIT-Q4_PROFIT)  AS profit_decline,
ROUND((((Q3_PROFIT-Q4_PROFIT)/Q3_PROFIT)*100),2) AS percentage_decline
FROM merge
ORDER BY  profit_decline DESC;

SELECT
    region,
    ROUND(SUM(CASE WHEN quarter = 3 THEN profit ELSE 0 END), 2) AS q3_profit,
    ROUND(SUM(CASE WHEN quarter = 4 THEN profit ELSE 0 END), 2) AS q4_profit,

    ROUND(
        SUM(CASE WHEN quarter = 3 THEN profit ELSE 0 END)
        -
        SUM(CASE WHEN quarter = 4 THEN profit ELSE 0 END),
        2
    ) AS profit_decline,

    ROUND(
        (
            (
                SUM(CASE WHEN quarter = 3 THEN profit ELSE 0 END)
                -
                SUM(CASE WHEN quarter = 4 THEN profit ELSE 0 END)
            )
            /
            NULLIF(SUM(CASE WHEN quarter = 3 THEN profit ELSE 0 END), 0)
        ) * 100,
        2
    ) AS percentage_decline

FROM ecommerce_cleaned
WHERE quarter IN (3, 4)
GROUP BY region
ORDER BY profit_decline DESC
LIMIT 1;



-- 2. Top 5 Products by Revenue Within Each Category — Window Function

-- Question:
-- Find the top 5 products by revenue within each product category.
WITH rev AS (SELECT category,product_name,
SUM(net_revenue) AS  revenue
FROM ecommerce_cleaned
GROUP BY category,product_name),

ranked AS 
(SELECT category,product_name,revenue,DENSE_RANK()OVER(PARTITION BY CATEGORY
ORDER BY revenue DESC) AS ranking
FROM rev
)

SELECT category,product_name,revenue,ranking
FROM ranked 
WHERE ranking <=5;

-- 3. Customers Spending Above Their Regional Average 
-- Question:
-- Find customers whose total spending is greater than the average customer spending in their region.


WITH spends AS (SELECT region ,customer_id, customer_name ,SUM(net_revenue)AS customer_spending
FROM ecommerce_cleaned
GROUP BY region, customer_id ,customer_name),
region_avg AS(
SELECT region ,customer_id, customer_name, customer_spending, AVG(customer_spending)OVER (PARTITION BY region) AS reg_avg
FROM spends)

SELECT  region ,customer_id, customer_name, customer_spending, reg_avg
FROM region_avg
WHERE customer_spending >  reg_avg
ORDER BY region, customer_spending DESC;

-- 4. Month-over-Month Revenue Decline 

-- Question:
-- Identify all months where revenue declined compared with the previous month.

WITH rev_dec AS(SELECT `month`,SUM(net_revenue) AS revenue,LAG(SUM(net_revenue)) OVER (ORDER BY  `month` ) AS previous_month_revenue
FROM ecommerce_cleaned
GROUP BY `month`
)
SELECT  `month`,revenue, 
previous_month_revenue,
(revenue-previous_month_revenue) AS rev_change, 
ROUND((((revenue-previous_month_revenue)/previous_month_revenue)*100),2) AS change_pct
FROM rev_dec
WHERE revenue < previous_month_revenue
ORDER BY `month`;




-- 5. Customers With Increasing Purchase Frequency — Window Function

-- Question:
-- Identify customers whose number of orders increased for at least 2 consecutive months.

WITH monthly_orders AS (
    SELECT
        customer_id,
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        COUNT(DISTINCT order_id) AS orders
    FROM ecommerce_cleaned
    GROUP BY
        customer_id,
        DATE_FORMAT(order_date, '%Y-%m')
),

order_growth AS (
    SELECT
        customer_id,
        month,
        orders,
        LAG(orders) OVER (
            PARTITION BY customer_id
            ORDER BY month
        ) AS previous_month_orders
    FROM monthly_orders
),

growth_check AS (
    SELECT
        customer_id,
        month,
        orders,
        previous_month_orders,
        CASE
            WHEN orders > previous_month_orders THEN 1
            ELSE 0
        END AS increased
    FROM order_growth
),

consecutive_growth AS (
    SELECT
        customer_id,
        month,
        increased,
        LAG(increased) OVER (
            PARTITION BY customer_id
            ORDER BY month
        ) AS previous_increased
    FROM growth_check
)

SELECT DISTINCT
    customer_id
FROM consecutive_growth
WHERE increased = 1
  AND previous_increased = 1;

-- 6. Products With Above-Average Return Rate — Subquery

-- Question:
-- Find products whose return rate is higher than the overall product-level average return rate.
WITH product_returns AS (
    SELECT
        product_name,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(
            DISTINCT CASE
                WHEN return_status = 'Yes' THEN order_id
            END
        ) AS returned_orders,
        ROUND(
            COUNT(
                DISTINCT CASE
                    WHEN return_status = 'Yes' THEN order_id
                END
            ) / COUNT(DISTINCT order_id) * 100,
            2
        ) AS return_rate
    FROM ecommerce_cleaned
    GROUP BY product_name
),

avg_return AS (
    SELECT
        AVG(return_rate) AS average_return_rate
    FROM product_returns
)

SELECT
    p.product_name,
    p.total_orders,
    p.returned_orders,
    p.return_rate,
    ROUND(a.average_return_rate, 2) AS average_return_rate
FROM product_returns p
CROSS JOIN avg_return a
WHERE p.return_rate > a.average_return_rate
ORDER BY p.return_rate DESC;


-- 7. Revenue Contribution by Region — Window Function

-- Question:
-- Calculate each region's revenue contribution to total company revenue.

WITH regional_revenue AS (
    SELECT
        region,
        SUM(net_revenue) AS revenue
    FROM ecommerce_cleaned
    GROUP BY region
)

SELECT
    region,
    revenue,
    SUM(revenue) OVER () AS company_revenue,
    ROUND(
        revenue / SUM(revenue) OVER () * 100,
        2
    ) AS revenue_percentage
FROM regional_revenue
ORDER BY revenue DESC;






-- 8. Identify Repeat Customers — CTE + Window Function

-- Question:
-- Find customers who placed at least 3 orders, and calculate the average number of days between their purchases.

WITH customer_orders AS (
    SELECT DISTINCT
        customer_id,
        order_id,
        order_date
    FROM ecommerce_cleaned
),

purchase_gaps AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        LAG(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS previous_order_date
    FROM customer_orders
),

customer_summary AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        AVG(
            DATEDIFF(order_date, previous_order_date)
        ) AS avg_days_between_orders
    FROM purchase_gaps
    GROUP BY customer_id
)

SELECT
    customer_id,
    total_orders,
    ROUND(avg_days_between_orders, 2) AS avg_days_between_orders
FROM customer_summary
WHERE total_orders >= 3
ORDER BY total_orders DESC;






