import pandas as pd
from app.core.config import DATA_PATH
from app.services.fuzzy_engine import assess_risk

def get_all_suppliers():
    df = pd.read_csv(DATA_PATH)
    records = df.to_dict(orient="records")

    assessed = []
    for row in records:
        risk_result = assess_risk(
            row["supplier_reliability"],
            row["transportation_delay_risk"],
            row["demand_uncertainty"],
        )
        assessed.append({**row, **risk_result})

    return assessed

def get_summary():
    data = get_all_suppliers()
    total = len(data)
    avg_score = round(sum(item["overall_risk_score"] for item in data) / total, 2) if total else 0

    counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for item in data:
        counts[item["overall_risk_level"]] += 1

    return {
        "total_suppliers": total,
        "average_overall_risk_score": avg_score,
        "risk_distribution": counts,
    }