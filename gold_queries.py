import duckdb

con = duckdb.connect("olist.duckdb", read_only=True)

queries = [
    ("1. How many orders are there in each status?",
     """
     SELECT order_status, COUNT(*) AS num_orders
     FROM orders
     GROUP BY order_status
     ORDER BY num_orders DESC
     """),

    ("2. Which 10 product categories earn the most revenue (delivered orders)?",
     """
     SELECT t.product_category_name_english AS category,
            ROUND(SUM(oi.price), 2) AS revenue
     FROM order_items oi
     JOIN orders o ON oi.order_id = o.order_id
     JOIN products p ON oi.product_id = p.product_id
     JOIN product_category_name_translation t
          ON p.product_category_name = t.product_category_name
     WHERE o.order_status = 'delivered'
     GROUP BY category
     ORDER BY revenue DESC
     LIMIT 10
     """),

    ("3. Which categories have the highest late-delivery rate (min 100 orders)?",
     """
     SELECT t.product_category_name_english AS category,
            COUNT(DISTINCT o.order_id) AS delivered_orders,
            ROUND(100.0 * COUNT(DISTINCT CASE
                WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                THEN o.order_id END) / COUNT(DISTINCT o.order_id), 2) AS late_pct
     FROM orders o
     JOIN order_items oi ON o.order_id = oi.order_id
     JOIN products p ON oi.product_id = p.product_id
     JOIN product_category_name_translation t
          ON p.product_category_name = t.product_category_name
     WHERE o.order_status = 'delivered'
       AND o.order_delivered_customer_date IS NOT NULL
     GROUP BY category
     HAVING COUNT(DISTINCT o.order_id) >= 100
     ORDER BY late_pct DESC
     LIMIT 10
     """),

    ("4. What is the monthly order count and revenue (delivered orders)?",
     """
     SELECT strftime(date_trunc('month', o.order_purchase_timestamp), '%Y-%m') AS month,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(oi.price), 2) AS revenue
     FROM orders o
     JOIN order_items oi ON o.order_id = oi.order_id
     WHERE o.order_status = 'delivered'
     GROUP BY month
     ORDER BY month
     """),

    ("5. Do late deliveries get worse review scores?",
     """
     SELECT CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                 THEN 'late' ELSE 'on_time' END AS delivery,
            COUNT(*) AS reviews,
            ROUND(AVG(r.review_score), 2) AS avg_score
     FROM orders o
     JOIN order_reviews r ON o.order_id = r.order_id
     WHERE o.order_status = 'delivered'
       AND o.order_delivered_customer_date IS NOT NULL
     GROUP BY delivery
     """),
]

for question, sql in queries:
    print("\n" + question)
    print(con.execute(sql).df().to_string(index=False))