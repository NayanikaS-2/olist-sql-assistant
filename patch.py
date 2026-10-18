import re

# ---- update eval.py ----
t = open("eval.py", encoding="utf-8").read()
if "results_{MODE}" not in t:
    t = t.replace("from ask import ask\n", "from ask import ask, MODE\n")
    t = t.replace('res.to_csv("results.csv", index=False)',
                  'res.to_csv(f"results_{MODE}.csv", index=False)')
    t = t.replace(r'print("\n=== ACCURACY ===")',
                  r'print(f"\n=== ACCURACY (mode: {MODE}) ===")')
    open("eval.py", "w", encoding="utf-8").write(t)
    print("eval.py updated")
else:
    print("eval.py was already updated")

# ---- update ask.py ----
a = open("ask.py", encoding="utf-8").read()
NEW = r'''import os
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
SYSTEM = "\n\n".join(parts)'''
if "MODE" not in a:
    a2 = re.sub(r'schema_doc = open\(.*?\{schema_doc\}"""', lambda m: NEW, a, flags=re.DOTALL)
    if a2 == a:
        print("WARNING: could not find the block in ask.py - tell Claude")
    else:
        open("ask.py", "w", encoding="utf-8").write(a2)
        print("ask.py updated")
else:
    print("ask.py was already updated")