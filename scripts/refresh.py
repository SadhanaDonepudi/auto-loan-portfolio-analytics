"""Automated refresh pattern: regenerate (or re-ingest) -> reload DB -> refresh outputs.
In production this would pull the latest ABS extract and refresh the Power BI
dataset via the Power BI REST API; here the synthetic generator stands in for the
source, and the Streamlit demo re-reads outputs/kpis.json on each load.
Schedule: daily, e.g. `0 6 * * * python run_all.py` (cron) or a Power BI scheduled refresh."""
import subprocess, sys, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if __name__ == "__main__":
    r = subprocess.run([sys.executable, os.path.join(BASE, "run_all.py")], check=False)
    print("refresh OK" if r.returncode == 0 else "refresh FAILED")
    sys.exit(r.returncode)
