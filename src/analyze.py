"""Analysis over a loans table (SQLite). Pure functions on DataFrames for testability."""
import pandas as pd

def headline(df):
    high = df[(df.term_months >= 72) & (df.credit_score < 640)]
    rest = df[~((df.term_months >= 72) & (df.credit_score < 640))]
    r_high = float(high.is_60d_delinquent.mean()) if len(high) else 0.0
    r_rest = float(rest.is_60d_delinquent.mean()) if len(rest) else 0.0
    return {"group": "72+ month & credit score < 640", "n": int(len(high)),
            "rate_60d": r_high, "comparison_n": int(len(rest)), "comparison_rate_60d": r_rest,
            "ratio": r_high / r_rest if r_rest else None}

def kpis(df):
    return {"n_loans": int(len(df)), "total_balance": float(df.orig_balance.sum()),
            "rate_60d": float(df.is_60d_delinquent.mean()),
            "rate_30d": float(df.is_30d_delinquent.mean()),
            "prepayment_rate": float(df.prepaid.mean()),
            "avg_credit_score": float(df.credit_score.mean()),
            "avg_rate": float(df.interest_rate.mean())}

def group_rates(df, col):
    g = df.groupby(col).agg(n=("loan_id", "count"), rate_60d=("is_60d_delinquent", "mean"),
                            prepayment_rate=("prepaid", "mean"), avg_balance=("orig_balance", "mean"),
                            avg_credit_score=("credit_score", "mean")).reset_index()
    return g
