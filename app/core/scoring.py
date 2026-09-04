import pandas as pd
from app.core.data_handler import parse_rent_int

def evaluate_listing(row: pd.Series, prefs: dict, budget: int):
    rent = parse_rent_int(row.get("negotiated_rent") or row.get("asking_rent"))
    if budget > 0 and rent > budget: return None
    
    score = 100
    for feature, pref_type in prefs.items():
        if pref_type == "No Preference": continue
        has_feature = "yes" in str(row.get(feature, "")).lower()
        if pref_type == "Must have" and not has_feature: return None
        elif pref_type == "Good to have" and has_feature: score += 10
        elif pref_type == "Absolutely should not have" and has_feature: return None
    return score

def process_listings(df_raw: pd.DataFrame, prefs: dict, budget: int) -> pd.DataFrame:
    scored_records = []
    for _, row in df_raw.iterrows():
        score = evaluate_listing(row, prefs, budget)
        if score is not None:
            row_dict = row.to_dict()
            row_dict["match_score"] = score
            scored_records.append(row_dict)
    return pd.DataFrame(scored_records).sort_values(by="match_score", ascending=False)