# Data Model
- **Fact table `Loans`** (one row per loan): loan_id (key), vintage, term_months, vehicle_type,
  credit_score, credit_band, orig_balance, interest_rate, is_30d_delinquent, is_60d_delinquent, prepaid.
- **Dimension tables** (derived, for slicers): DimVintage (2020–2025), DimTerm (36/48/60/72/84),
  DimVehicle (New/Used), DimCreditBand (<580 … 720+). Each relates 1-to-many to Loans.
- Relationships are single-direction (dimension → fact) so slicers filter all visuals.
- Grain: loan level. All measures in DAX_measures.dax aggregate from this grain; no pre-aggregation.
