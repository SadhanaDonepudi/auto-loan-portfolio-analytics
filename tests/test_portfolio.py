import sys, os, sqlite3, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from generate import generate
from analyze import headline, kpis, group_rates

def test_generate_schema_and_bands():
    df = generate(n=5000)
    assert len(df) == 5000
    assert set(df.credit_band) <= {"<580", "580-639", "640-679", "680-719", "720+"}
    assert df.term_months.isin([36, 48, 60, 72, 84]).all()
    assert df.vehicle_type.isin(["New", "Used"]).all()
    assert df.is_60d_delinquent.isin([0, 1]).all()

def test_kpis_and_headline_bounds():
    df = generate(n=20000)
    k = kpis(df); h = headline(df)
    assert 0 < k["rate_60d"] < 0.2 and 0 <= k["prepayment_rate"] <= 1
    assert h["n"] > 0 and h["ratio"] is not None and h["ratio"] > 1  # long subprime terms riskier by construction
    assert h["rate_60d"] > h["comparison_rate_60d"]

def test_sql_loads_and_queries():
    df = generate(n=3000)
    conn = sqlite3.connect(":memory:")
    conn.executescript(open(os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql")).read())
    df.to_sql("loans", conn, if_exists="append", index=False)
    n = conn.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
    assert n == 3000
    row = conn.execute("SELECT AVG(is_60d_delinquent) FROM loans WHERE term_months>=72 AND credit_score<640").fetchone()
    assert 0 <= row[0] <= 1
    conn.close()

def test_group_rates_complete():
    df = generate(n=5000)
    for col in ["vintage", "term_months", "vehicle_type", "credit_band"]:
        g = group_rates(df, col)
        assert len(g) > 1 and "rate_60d" in g.columns

def test_dax_and_memo_exist():
    base = os.path.join(os.path.dirname(__file__), "..")
    dax = open(os.path.join(base, "docs", "powerbi", "DAX_measures.dax")).read()
    for m in ["Total Loans", "Delinquency Rate 60D", "Prepayment Rate"]:
        assert m in dax
    memo = open(os.path.join(base, "docs", "memo.md")).read()
    assert memo.count("## Insight") == 3
