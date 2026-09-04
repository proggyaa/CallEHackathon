from pathlib import Path
import re
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).parent.parent.parent / "listings.db"
PREF_OPTIONS = ["No Preference", "Must have", "Good to have", "Absolutely should not have"]

@st.cache_data(ttl=5)
def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM listings ORDER BY called_at DESC", conn)

def format_currency(val, default="$0") -> str:
    if pd.isna(val) or val is None or val == "": return default
    val_str = str(val).strip()
    if val_str.startswith("$"): return val_str
    nums = re.sub(r"[^\d]", "", val_str)
    return f"${int(nums):,}" if nums else default

def parse_rent_int(val) -> int:
    if pd.isna(val) or val is None or val == "": return 0
    nums = re.sub(r"[^\d]", "", str(val))
    return int(nums) if nums else 0