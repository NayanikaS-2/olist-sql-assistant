HARD_TESTS = [
    ("medium", "What percentage of delivered orders arrived after the estimated delivery date? Only count delivered orders that have a delivery date. Round to 2 decimals.",
     """SELECT ROUND(100.0 * SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END) / COUNT(*), 2)
        FROM orders
        WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL"""),

    ("medium", "How many orders were placed in 2017?",
     "SELECT COUNT(*) FROM orders WHERE EXTRACT(year FROM order_purchase_timestamp) = 2017"),

    ("medium", "How many orders contain more than one item?",
     """SELECT COUNT(*) FROM (
          SELECT order_id FROM order_items GROUP BY order_id HAVING COUNT(*) > 1)"""),

    ("medium", "How many orders have no review at all?",
     """SELECT COUNT(*) FROM orders o
        LEFT JOIN order_reviews r ON o.order_id = r.order_id
        WHERE r.order_id IS NULL"""),

    ("medium", "How many delivered orders were purchased on a weekend (Saturday or Sunday)?",
     """SELECT COUNT(*) FROM orders
        WHERE order_status = 'delivered'
          AND EXTRACT(dow FROM order_purchase_timestamp) IN (0, 6)"""),

    ("medium", "Which seller has the most distinct orders? Show seller_id and the number of orders.",
     """SELECT seller_id, COUNT(DISTINCT order_id) AS n
        FROM order_items GROUP BY seller_id ORDER BY n DESC LIMIT 1"""),

    ("hard", "Which 5 customer states have the highest average freight_value per item? Show state and average rounded to 2 decimals.",
     """SELECT c.customer_state, ROUND(AVG(oi.freight_value), 2) AS a
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY 1 ORDER BY a DESC LIMIT 5"""),

    ("hard", "What is the average review score for late versus on-time deliveries? Only delivered orders with a delivery date. Show only two columns: a label that is exactly 'late' or 'on_time', and the average score rounded to 2 decimals.",
     """SELECT CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'late' ELSE 'on_time' END AS delivery,
               ROUND(AVG(r.review_score), 2)
        FROM orders o JOIN order_reviews r ON o.order_id = r.order_id
        WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
        GROUP BY 1"""),

    ("hard", "Which month (as text like 2017-11) had the highest revenue from delivered orders? Revenue is the sum of item price. Show month and revenue rounded to 2 decimals.",
     """SELECT strftime(date_trunc('month', o.order_purchase_timestamp), '%Y-%m') AS month,
               ROUND(SUM(oi.price), 2) AS rev
        FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY 1 ORDER BY rev DESC LIMIT 1"""),

    ("hard", "How many real customers (customer_unique_id) placed more than one order?",
     """SELECT COUNT(*) FROM (
          SELECT c.customer_unique_id
          FROM orders o JOIN customers c ON o.customer_id = c.customer_id
          GROUP BY 1 HAVING COUNT(DISTINCT o.order_id) > 1)"""),

    ("hard", "Which product category (English name) has the lowest average review score? Show category and average rounded to 2 decimals.",
     """SELECT t.product_category_name_english, ROUND(AVG(r.review_score), 2) AS s
        FROM order_reviews r
        JOIN order_items oi ON r.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
        GROUP BY 1 ORDER BY s ASC LIMIT 1"""),

    ("hard", "For all orders, what are the top 3 customer states by revenue (sum of item price), and what percent of total revenue does each represent? Show state, revenue and percent, rounded to 2 decimals.",
     """SELECT c.customer_state, ROUND(SUM(oi.price), 2) AS rev,
               ROUND(100.0 * SUM(oi.price) / SUM(SUM(oi.price)) OVER (), 2) AS share
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY 1 ORDER BY rev DESC LIMIT 3"""),
]