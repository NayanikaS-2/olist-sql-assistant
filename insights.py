import duckdb

con = duckdb.connect("olist.duckdb", read_only=True)

queries = [
    ("A. Late vs on-time deliveries: share of orders and review score",
     """
     SELECT CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                 THEN 'late' ELSE 'on_time' END AS delivery,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(100.0 * COUNT(DISTINCT o.order_id) / SUM(COUNT(DISTINCT o.order_id)) OVER (), 2) AS pct_of_orders,
            ROUND(AVG(r.review_score), 2) AS avg_score
     FROM orders o JOIN order_reviews r ON o.order_id = r.order_id
     WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
     GROUP BY 1
     """),

    ("B. Repeat customers: how many real customers ordered more than once",
     """
     SELECT COUNT(*) AS total_customers,
            SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END) AS repeat_customers,
            ROUND(100.0 * SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_pct
     FROM (SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS n
           FROM orders o JOIN customers c ON o.customer_id = c.customer_id
           GROUP BY 1)
     """),

    ("C. Late-delivery rate by customer state (worst 5, states with 500+ orders)",
     """
     SELECT c.customer_state,
            COUNT(*) AS delivered_orders,
            ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                                   THEN 1 ELSE 0 END) / COUNT(*), 2) AS late_pct
     FROM orders o JOIN customers c ON o.customer_id = c.customer_id
     WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
     GROUP BY 1 HAVING COUNT(*) >= 500
     ORDER BY late_pct DESC LIMIT 5
     """),

    ("D. Revenue concentration: top 5 states share of total item revenue",
     """
     SELECT c.customer_state,
            ROUND(SUM(oi.price), 2) AS revenue,
            ROUND(100.0 * SUM(oi.price) / SUM(SUM(oi.price)) OVER (), 2) AS share_pct
     FROM order_items oi
     JOIN orders o ON oi.order_id = o.order_id
     JOIN customers c ON o.customer_id = c.customer_id
     GROUP BY 1 ORDER BY revenue DESC LIMIT 5
     """),
]

for title, sql in queries:
    print("\n" + title)
    print(con.execute(sql).df().to_string(index=False))