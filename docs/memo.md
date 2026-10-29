# MEMO — Auto Loan Portfolio: What the Data Says (1 page)
**To:** Business leadership (non-technical audience) · **Subject:** Delinquency risk in our auto loan portfolio
**Data:** 520,000 synthetic loan-level records (seed 42). These are simulated loans, NOT real SEC EDGAR / Reg AB II filings — the patterns below illustrate how this analysis works, not real portfolio performance.

## Insight 1 — Long loans to lower-score borrowers carry the most risk
Loans of 72 months or longer to borrowers with credit scores under 640 default to 60-day delinquency at **10.38%**, versus **4.95%** for all other loans — about **2.10x** as high. Action: tighten approval or pricing for new 72+ month loans under 640 (larger down payment, shorter term offer, or added verification), and put existing ones on an early-watch list.

## Insight 2 — Credit score is the single strongest risk signal
60-day delinquency falls steadily as scores rise: **11.80%** (under 580), **8.86%** (580–639), **5.76%** (640–679), **3.95%** (680–719), **2.67%** (720+). Action: use score bands, not a single cutoff, when setting rates and reserves — the jump between 640–679 and 680–719 alone is worth pricing separately.

## Insight 3 — Used vehicles and longer terms deserve closer monitoring, not panic
Used-vehicle loans run at **5.88%** 60-day delinquency vs **5.14%** for new vehicles, and 72+/84-month terms at ~**6.6%** vs ~**4.8–4.9%** for 36–60-month terms — real but smaller gaps than the score effect. Prepayment is healthy overall (**13.39%**) and highest for high-score, short-term borrowers (16%+). Action: monitor used-vehicle and long-term segments monthly on the dashboard, but focus intervention (Insight 1) where risk concentrates.
