"""Generate synthetic loan-level auto loan data (seed 42). No real filings."""
import numpy as np, pandas as pd

N_DEFAULT = 520_000
CREDIT_BANDS = ["<580", "580-639", "640-679", "680-719", "720+"]
CREDIT_P = [0.08, 0.17, 0.25, 0.25, 0.25]
CREDIT_BASE_60D = {"<580": 0.105, "580-639": 0.075, "640-679": 0.045, "680-719": 0.026, "720+": 0.013}

def generate(n=N_DEFAULT, seed=42):
    rng = np.random.default_rng(seed)
    vintage = rng.choice([2020, 2021, 2022, 2023, 2024, 2025], size=n, p=[0.12, 0.16, 0.18, 0.20, 0.19, 0.15])
    term = rng.choice([36, 48, 60, 72, 84], size=n, p=[0.10, 0.18, 0.32, 0.28, 0.12])
    vehicle = rng.choice(["New", "Used"], size=n, p=[0.45, 0.55])
    band = rng.choice(CREDIT_BANDS, size=n, p=CREDIT_P)
    base = np.array([CREDIT_BASE_60D[b] for b in band])
    # Risk adjustments (documented model assumptions, not fitted to any resume claim)
    p60 = base + np.where(term >= 72, 0.018, 0.0) + np.where(vehicle == "Used", 0.008, 0.0)
    p60 += np.where(vintage >= 2023, 0.004, 0.0)  # recent vintages slightly worse (synthetic)
    p60 = np.clip(p60, 0.001, 0.35)
    is_60d = rng.random(n) < p60
    is_30d = is_60d | (rng.random(n) < 0.012)  # 30-day bucket includes 60-day loans
    # Prepayment: higher for high credit / shorter terms / new vehicles
    p_pre = np.where(np.isin(band, ["720+", "680-719"]), 0.16, 0.10) + np.where(term <= 48, 0.04, 0.0)
    prepaid = (rng.random(n) < p_pre) & ~is_60d
    balance = np.where(vehicle == "New",
                       rng.normal(32000, 8000, n), rng.normal(19000, 6000, n)).clip(3000, 90000).round(2)
    rate = np.array([9.8 if b in ("<580", "580-639") else 7.2 if b == "640-679" else 5.4 if b == "680-719" else 4.1 for b in band]) \
        + rng.normal(0, 1.1, n)
    score_mid = {"<580": 550, "580-639": 610, "640-679": 660, "680-719": 700, "720+": 750}
    score = np.array([score_mid[b] for b in band]) + rng.integers(-25, 26, n)
    return pd.DataFrame({
        "loan_id": [f"L{i:07d}" for i in range(1, n + 1)],
        "vintage": vintage, "term_months": term, "vehicle_type": vehicle,
        "credit_score": score, "credit_band": band,
        "orig_balance": balance.round(2),
        "interest_rate": rate.clip(2.0, 18.0).round(2),
        "is_30d_delinquent": is_30d.astype(int), "is_60d_delinquent": is_60d.astype(int),
        "prepaid": prepaid.astype(int),
    })

if __name__ == "__main__":
    df = generate()
    print(f"rows={len(df)} 60d_rate={df.is_60d_delinquent.mean():.4f}")
