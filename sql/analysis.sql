-- Portfolio KPIs
SELECT COUNT(*) AS n_loans, SUM(orig_balance) AS total_balance,
       AVG(is_60d_delinquent) AS rate_60d, AVG(is_30d_delinquent) AS rate_30d,
       AVG(prepaid) AS prepayment_rate, AVG(credit_score) AS avg_credit_score
FROM loans;
-- Headline: 72+ month & score < 640 vs all other loans (60-day delinquency)
SELECT '72+mo & score<640' AS grp, COUNT(*) AS n, AVG(is_60d_delinquent) AS rate_60d FROM loans
WHERE term_months >= 72 AND credit_score < 640
UNION ALL
SELECT 'all other loans', COUNT(*), AVG(is_60d_delinquent) FROM loans
WHERE NOT (term_months >= 72 AND credit_score < 640);
-- Trends by vintage / term / vehicle type / credit band
SELECT vintage, COUNT(*) AS n, AVG(is_60d_delinquent) AS rate_60d, AVG(prepaid) AS prepay FROM loans GROUP BY vintage ORDER BY vintage;
SELECT term_months, COUNT(*) AS n, AVG(is_60d_delinquent) AS rate_60d, AVG(prepaid) AS prepay FROM loans GROUP BY term_months ORDER BY term_months;
SELECT vehicle_type, COUNT(*) AS n, AVG(is_60d_delinquent) AS rate_60d, AVG(prepaid) AS prepay FROM loans GROUP BY vehicle_type;
SELECT credit_band, COUNT(*) AS n, AVG(is_60d_delinquent) AS rate_60d, AVG(prepaid) AS prepay FROM loans GROUP BY credit_band;
