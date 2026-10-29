"""Streamlit demo of the portfolio KPIs (Power BI Desktop unavailable locally;
the DAX spec in docs/powerbi/ is the production dashboard definition)."""
import json, os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

def main():
    import streamlit as st
    st.title("Auto Loan Portfolio Analytics — Self-Service Dashboard (Synthetic Data)")
    with open(os.path.join(BASE, "outputs", "kpis.json")) as f:
        k = json.load(f)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Loans", f"{k['n_loans']:,}"); c2.metric("Total balance", f"${k['total_balance']:,.0f}")
    c3.metric("60-day delinquency", f"{k['rate_60d']:.2%}"); c4.metric("Prepayment rate", f"{k['prepayment_rate']:.2%}")
    h = k["headline"]
    st.subheader("Headline comparison")
    st.write(f"72+ month & score < 640: {h['rate_60d']:.2%} (n={h['n']:,}) vs all other loans: "
             f"{h['comparison_rate_60d']:.2%} — ratio {h['ratio']:.2f}x")
    for name, title in [("by_vintage", "By vintage"), ("by_term", "By term"),
                        ("by_vehicle", "By vehicle type"), ("by_credit_band", "By credit band")]:
        st.subheader(title)
        st.dataframe(pd.read_csv(os.path.join(BASE, "outputs", f"{name}.csv")))
        st.caption("Filters: use the sidebar in Power BI (see docs/powerbi/); this demo shows the same KPI tables.")

if __name__ == "__main__":
    main()
