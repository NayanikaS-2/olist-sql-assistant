import pandas as pd

files = {
    "1. No context": "results_none.csv",
    "2. Exact schema only": "results_schema_only.csv",
    "3. Schema + dictionary": "results_run2.csv",
}
rows = []
for label, f in files.items():
    try:
        r = pd.read_csv(f)
    except FileNotFoundError:
        print("missing:", f)
        continue
    ok = r["status"] == "PASS"
    row = {"setup": label, "overall": f"{ok.mean():.0%} ({ok.sum()}/{len(r)})"}
    for d in ["easy", "medium", "hard"]:
        s = ok[r["difficulty"] == d]
        row[d] = f"{s.mean():.0%}" if len(s) else "-"
    rows.append(row)

print(pd.DataFrame(rows).to_string(index=False))