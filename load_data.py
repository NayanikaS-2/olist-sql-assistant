import duckdb, glob, os

con = duckdb.connect("olist.duckdb")

for f in glob.glob("data/*.csv"):
    name = os.path.basename(f).replace("olist_", "").replace("_dataset.csv", "").replace(".csv", "")
    con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{f}')")
    rows = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"{name}: {rows} rows")

con.close()