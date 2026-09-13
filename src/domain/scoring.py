import re
import pandas as pd

# app/core/scoring.py

def evaluate_listing_color(call_result: dict, user_must_haves: list) -> str:
    """
    Evaluates stored call extraction data dynamically against current active user must-haves.
    Returns background hex color code:
    - #A4CE8B (Green): All active must-haves are confirmed/non-negotiable for landlord
    - #FFBE91 (Orange): Must-haves are listed as negotiable by landlord
    - #9E3B3B (Red): Any active must-have is non-negotiable / rejected by landlord
    """
    if not call_result or not user_must_haves:
        return "#FFFFFF"  # Default white card if no call results or no active must-haves
    
    # Extract landlord feature classifications from call extraction payload
    # Example format: {"Parking Available": "confirmed", "Pet Policy Allowed": "non_negotiable"}
    landlord_amenities = call_result.get("amenities", {})

    status_colors = []
    
    for feature in user_must_haves:
        landlord_stance = landlord_amenities.get(feature, "unknown").lower()
        
        # If landlord flatly rejects/disallows a must-have -> Instant Red
        if landlord_stance in ["non_negotiable", "rejected", "unavailable", "no"]:
            return "#9E3B3B"
        
        # If landlord offers it under negotiation -> Mark Orange priority
        elif landlord_stance in ["negotiable", "conditional", "partial"]:
            status_colors.append("#FFBE91")
            
        # If landlord confirms availability -> Green stance
        elif landlord_stance in ["confirmed", "available", "yes"]:
            status_colors.append("#A4CE8B")

    # If any feature was negotiable, return Orange; otherwise Green
    if "#FFBE91" in status_colors:
        return "#FFBE91"
        
    return "#A4CE8B" if status_colors else "#FFFFFF"

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