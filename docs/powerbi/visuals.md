# Dashboard Visuals, Drill-Downs & Filters
- **KPI cards (top):** Total Loans, Total Balance, 60-day delinquency rate, prepayment rate, average credit score.
- **Line chart:** 60-day delinquency by vintage (2020–2025) with drill-down vintage → credit band.
- **Bar chart:** 60-day delinquency by term, with drill-down term → vehicle type.
- **Stacked bar:** delinquency by credit band, split New vs Used.
- **Table:** headline comparison — 72+ month & score < 640 vs all other loans.
- **Filters/slicers:** vintage, term, vehicle type, credit band; a "High-risk only" button (term ≥ 72 AND score < 640).
- **Refresh:** scripts/refresh.py regenerates data and outputs daily; in production, Power BI scheduled refresh would point at the PostgreSQL warehouse instead of the local SQLite file.
