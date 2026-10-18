import duckdb

con = duckdb.connect("olist.duckdb", read_only=True)

sql = """
SELECT order_status, COUNT(*) AS num_orders
FROM orders
GROUP BY order_status
ORDER BY num_orders DESC
"""

print(con.execute(sql).df())