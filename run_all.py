"""End-to-end reproducible run: generate -> SQLite -> SQL analysis -> outputs.
Large intermediates go to /tmp; only small summary outputs are committed."""
import json, sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from generate import generate
from analyze import headline, kpis, group_rates

BASE = os.path.dirname(os.path.abspath(__file__))
DB = "/tmp/auto_loans.db"

def main():
    df = generate()
    print(f"Generated {len(df):,} synthetic loans")
    conn = sqlite3.connect(DB)
    with open(os.path.join(BASE, "sql", "schema.sql")) as f:
        conn.executescript(f.read())
    conn.execute("DELETE FROM loans")
    df.to_sql("loans", conn, if_exists="append", index=False)
    conn.commit()
    # Verify via the SQL file's headline query shape (run from Python for JSON output)
    out = kpis(df); out["headline"] = headline(df)
    os.makedirs(os.path.join(BASE, "outputs"), exist_ok=True)
    for name, col in [("by_vintage", "vintage"), ("by_term", "term_months"),
                      ("by_vehicle", "vehicle_type"), ("by_credit_band", "credit_band")]:
        group_rates(df, col).to_csv(os.path.join(BASE, "outputs", f"{name}.csv"), index=False)
    # Small sample for repo inspection (first 1000 rows only; full data regenerates)
    df.head(1000).to_csv(os.path.join(BASE, "outputs", "sample_1000.csv"), index=False)
    with open(os.path.join(BASE, "outputs", "kpis.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    conn.close()

if __name__ == "__main__":
    main()
