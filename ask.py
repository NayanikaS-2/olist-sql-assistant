import duckdb, re
from google import genai

MODEL = "gemini-flash-lite-latest"
con = duckdb.connect("olist.duckdb", read_only=True)
client = genai.Client()
import os
MODE = os.environ.get("MODE", "full")

schema_doc = open("data_dictionary.md", encoding="utf-8").read()
real_schema = "\n".join(
    f"{t[0]}({', '.join(c[0] for c in con.execute('DESCRIBE ' + t[0]).fetchall())})"
    for t in con.execute("SHOW TABLES").fetchall()
)

parts = ["You are a data analyst writing DuckDB SQL. Return ONLY one SQL SELECT query. No explanation, no markdown."]
if MODE in ("full", "schema_only"):
    parts.append("Use ONLY the exact table and column names listed under EXACT SCHEMA. Never invent names.\n\nEXACT SCHEMA:\n" + real_schema)
if MODE == "full":
    parts.append("DESCRIPTION OF THE DATA:\n" + schema_doc)
SYSTEM = "\n\n".join(parts)

def clean(text):
    return re.sub(r"```(?:sql)?", "", text or "").strip().rstrip(";")

def check(sql):
    s = sql.lower()
    if not (s.startswith("select") or s.startswith("with")):
        raise ValueError("Only SELECT queries are allowed")
    for bad in ["insert", "update", "delete", "drop", "alter", "create", "attach", "copy"]:
        if re.search(rf"\b{bad}\b", s):
            raise ValueError(f"Forbidden keyword: {bad}")

def ask_llm(messages):
    contents = [
        {"role": "model" if m["role"] == "assistant" else "user",
         "parts": [{"text": m["content"]}]}
        for m in messages
    ]
    r = client.models.generate_content(
        model=MODEL, contents=contents,
        config={"system_instruction": SYSTEM},
    )
    return clean(r.text)

def ask(question):
    messages = [{"role": "user", "content": question}]
    sql = ask_llm(messages)
    for attempt in range(2):
        try:
            check(sql)
            df = con.execute(f"SELECT * FROM ({sql}) LIMIT 200").df()
            return sql, df
        except Exception as e:
            if attempt == 1:
                raise
            messages += [
                {"role": "assistant", "content": sql},
                {"role": "user", "content": f"That query failed with: {e}\nReturn a corrected SQL query only."},
            ]
            sql = ask_llm(messages)

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type quit): ")
        if q.strip().lower() == "quit":
            break
        try:
            sql, df = ask(q)
            print("\nSQL used:\n" + sql)
            print("\nResult:")
            print(df.to_string(index=False))
        except Exception as e:
            print("Failed:", e)