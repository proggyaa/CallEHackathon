import re
import pandas as pd

def evaluate_listing(row, prefs=None, budget=0):
    prefs = prefs or {}
    
    # Safely extract and clean rent values regardless of type (string, list, int)
    rent_raw = row.get("rent", 0)
    if isinstance(rent_raw, list):
        rent_raw = rent_raw[0] if len(rent_raw) > 0 else 0
        
    if isinstance(rent_raw, str):
        cleaned = re.sub(r'[^\d]', '', rent_raw)
        rent = int(cleaned) if cleaned else 0
    elif isinstance(rent_raw, (int, float)):
        rent = int(rent_raw)
    else:
        rent = 0

    # Ensure budget is numeric if passed incorrectly
    if not isinstance(budget, (int, float)):
        budget = 0

    if budget > 0 and rent > budget:
        return None

    return row

def process_listings(df, prefs=None, budget=0):
    if df.empty:
        return df

    processed = []
    for idx, row in df.iterrows():
        evaluated = evaluate_listing(row, prefs, budget)
        if evaluated is not None:
            processed.append(evaluated)
            
    return pd.DataFrame(processed) if processed else pd.DataFrame(columns=df.columns)