import time, numbers
import duckdb
import pandas as pd
from ask import ask, MODE

gold_con = duckdb.connect("olist.duckdb", read_only=True)

TESTS = [
    ("easy", "How many orders were delivered?",
     "SELECT COUNT(*) FROM orders WHERE order_status = 'delivered'"),

    ("easy", "How many unique customers (real people) are there?",
     "SELECT COUNT(DISTINCT customer_unique_id) FROM customers"),

    ("easy", "What is the average review score?",
     "SELECT ROUND(AVG(review_score), 2) FROM order_reviews"),

    ("easy", "Which 5 states have the most unique customers? Show state and count.",
     """SELECT customer_state, COUNT(DISTINCT customer_unique_id) AS n
        FROM customers GROUP BY customer_state ORDER BY n DESC LIMIT 5"""),

    ("medium", "What is the total payment value for each payment type?",
     """SELECT payment_type, ROUND(SUM(payment_value), 2)
        FROM order_payments GROUP BY payment_type"""),

    ("medium", "Which 5 sellers have the highest total revenue (sum of item price)? Show seller_id and revenue.",
     """SELECT seller_id, ROUND(SUM(price), 2) AS revenue
        FROM order_items GROUP BY seller_id ORDER BY revenue DESC LIMIT 5"""),

    ("hard", "Which 5 product categories (English names) have the most items sold? Show category and item count.",
     """SELECT t.product_category_name_english, COUNT(*) AS items
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN product_category_name_translation t
             ON p.product_category_name = t.product_category_name
        GROUP BY 1 ORDER BY items DESC LIMIT 5"""),

    ("hard", "Which customer state has the highest average review score? Show state and score.",
     """SELECT c.customer_state, ROUND(AVG(r.review_score), 2) AS avg_score
        FROM order_reviews r
        JOIN orders o ON r.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY 1 ORDER BY avg_score DESC LIMIT 1"""),
]
from tests_hard import HARD_TESTS
TESTS = TESTS + HARD_TESTS

def norm(df):
    rows = []
    for row in df.itertuples(index=False):
        rows.append(tuple(
            round(float(v), 2) if isinstance(v, numbers.Number) else str(v)
            for v in row))
    return sorted(rows, key=str)

def ask_with_retry(q):
    for attempt in range(4):
        try:
            return ask(q)
        except Exception as e:
            msg = str(e)
            if ("503" in msg or "429" in msg) and attempt < 3:
                print("   server busy, waiting 30 seconds...")
                time.sleep(30)
            else:
                raise

results = []
for i, (difficulty, question, gold_sql) in enumerate(TESTS, 1):
    print(f"[{i}/{len(TESTS)}] {question}")
    sql, status = "", "FAIL"
    try:
        sql, df = ask_with_retry(question)
        gold_df = gold_con.execute(gold_sql).df()
        status = "PASS" if norm(df) == norm(gold_df) else "FAIL"
    except Exception as e:
        status = "ERROR"
        sql = str(e)[:200]
    print("   ->", status)
    results.append({"difficulty": difficulty, "question": question,
                    "status": status, "generated_sql": sql})
    time.sleep(7)

res = pd.DataFrame(results)
res["passed"] = res["status"] == "PASS"
res.to_csv(f"results_{MODE}.csv", index=False)

print(f"\n=== ACCURACY (mode: {MODE}) ===")
print(f"Overall: {res['passed'].mean():.0%} ({res['passed'].sum()}/{len(res)})")
print((res.groupby("difficulty")["passed"].mean() * 100).round(0).to_string())