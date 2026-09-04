from pathlib import Path
import re
import sqlite3
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(layout="wide", page_title="Flat Hunting Control Center")

# --- DATABASE LOGIC ---
DB_PATH = Path(__file__).parent.parent / "listings.db"

@st.cache_data(ttl=5)
def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM listings ORDER BY called_at DESC", conn)
    return df

df_raw = load_data()

# Custom Stark Error State (Replacing st.error)
if df_raw.empty:
    st.markdown("""
        <div style="background-color:#FFFFFF; border:2px solid #000000; border-radius:24px; padding:24px;">
            <div style="font-size:24px; font-weight:500; letter-spacing:-1px; margin-bottom:8px;">System Halted</div>
            <div style="font-size:14px; color:#555;">No listings found in the database. Execute prescreen_runner.py to populate data.</div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

def format_currency(val, default="$0"):
    if pd.isna(val) or val is None or val == "":
        return default
    val_str = str(val).strip()
    if val_str.startswith("$"):
        return val_str
    nums = re.sub(r"[^\d]", "", val_str)
    if nums:
        return f"${int(nums):,}"
    return default

def parse_rent_int(val) -> int:
    if pd.isna(val) or val is None or val == "":
        return 0
    nums = re.sub(r"[^\d]", "", str(val))
    return int(nums) if nums else 0

# --- "IMAGE_6EFF9F" VIBE STYLING + OVERRIDING NATIVE WIDGETS ---
st.markdown(
    """
    <style>
    /* Base Vibe */
    .stApp {
        background-color: #F8F9FA;
        font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
        color: #000000;
    }
    
    /* OVERRIDING STREAMLIT NATIVE INPUTS (The AI UI Fix) */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 30px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border-radius: 30px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: none !important;
    }
    label[data-testid="stWidgetLabel"] {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #000000 !important;
        margin-left: 8px !important;
    }
    
    /* Metric Cards */
    .metric-container {
        border-radius: 24px;
        padding: 24px;
        color: #000000;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        position: relative;
    }
    .metric-icon {
        position: absolute;
        top: 20px;
        left: 20px;
        background: #FFFFFF;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
    }
    .bg-mustard { background-color: #D2BE7B; }
    .bg-slate { background-color: #8DABBC; }
    .bg-orange { background-color: #F26531; }
    
    .metric-value { font-size: 36px; font-weight: 500; line-height: 1.1; margin-bottom: 4px; letter-spacing: -1px; }
    .metric-label { font-size: 13px; font-weight: 400; opacity: 0.9; }

    /* Property Cards */
    .property-card {
        background-color: #F2F3F5;
        border-radius: 28px;
        padding: 28px;
        margin-bottom: 24px;
        min-height: 260px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .prop-huge-val { font-size: 42px; font-weight: 500; letter-spacing: -1.5px; line-height: 1; margin: 16px 0; }
    .prop-title { font-size: 18px; font-weight: 500; }
    .prop-sub { font-size: 13px; color: #555; }
    
    /* Pill Buttons */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 30px !important; 
        font-size: 13px !important;
        font-weight: 500 !important;
        height: 36px !important;
        width: fit-content !important;
        padding: 0 20px !important;
    }
    div.stButton > button:hover {
        background-color: #EFEFEF !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- FILTERING (REMOVED EXPANDER, INLINE STARK STYLING) ---
st.markdown("<div style='font-size: 20px; font-weight: 500; letter-spacing: -0.5px; margin-bottom: 12px;'>Parameters</div>", unsafe_allow_html=True)

pref_options = ["No Preference", "Must have", "Good to have", "Absolutely should not have"]
col_p1, col_p2, col_p3, col_p4 = st.columns(4)
with col_p1:
    pet_pref = st.selectbox("Pet Policy", pref_options, index=0)
    parking_pref = st.selectbox("Parking", pref_options, index=0)
with col_p2:
    furnish_pref = st.selectbox("Furnished", pref_options, index=0)
    laundry_pref = st.selectbox("Laundry", pref_options, index=0)
with col_p3:
    dishwasher_pref = st.selectbox("Dishwasher", pref_options, index=0)
with col_p4:
    max_budget = st.number_input("Max Rent ($)", value=3000, step=100)

preferences = {
    "pet_policy": pet_pref, "parking_available": parking_pref,
    "furnishing_status": furnish_pref, "laundry": laundry_pref, "dishwasher": dishwasher_pref,
}

def evaluate_listing(row, prefs, budget):
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

scored_records = []
for idx, row in df_raw.iterrows():
    score = evaluate_listing(row, preferences, max_budget)
    if score is not None:
        row_dict = row.to_dict()
        row_dict["match_score"] = score
        scored_records.append(row_dict)

# Custom Stark Empty State (Replacing st.info)
if not scored_records:
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background-color:#E7DED8; border-radius:24px; padding:24px;">
            <div style="font-size:18px; font-weight:500; letter-spacing:-0.5px;">Zero Matches</div>
            <div style="font-size:14px; color:#333;">The current parameters yielded no results. Relax constraints to view listings.</div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(scored_records).sort_values(by="match_score", ascending=False)

# --- TOP METRICS ---
st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
total_calls = len(df)
tours_booked = int(df["tour_confirmed"].sum()) if "tour_confirmed" in df.columns else 0
conversion_rate = (tours_booked / total_calls * 100) if total_calls > 0 else 0

with m1:
    st.markdown(f"""
        <div class="metric-container bg-mustard">
            <div class="metric-icon">L</div>
            <div class="metric-value">{total_calls}</div>
            <div class="metric-label">Listings Prescreened</div>
        </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown(f"""
        <div class="metric-container bg-slate">
            <div class="metric-icon">T</div>
            <div class="metric-value">{tours_booked}</div>
            <div class="metric-label">Tours Secured</div>
        </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown(f"""
        <div class="metric-container bg-orange">
            <div class="metric-icon">%</div>
            <div class="metric-value">{conversion_rate:.0f}%</div>
            <div class="metric-label">Conversion Rate</div>
        </div>
    """, unsafe_allow_html=True)
with m4:
    st.markdown(f"""
        <div class="metric-container" style="background-color: #E7DED8;">
            <div class="metric-icon">A</div>
            <div class="metric-value">{df['match_score'].max()}</div>
            <div class="metric-label">Top Match Score</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# --- FLIP CARD GRID SYSTEM ---
if "card_states" not in st.session_state:
    st.session_state.card_states = {}

cols_per_row = 3
grid_cols = st.columns(cols_per_row, gap="large")

for idx, (_, row) in enumerate(df.iterrows()):
    col_idx = idx % cols_per_row
    listing_id = str(row.get("address", f"listing_{idx}"))

    if listing_id not in st.session_state.card_states:
        st.session_state.card_states[listing_id] = "front"

    is_front = st.session_state.card_states[listing_id] == "front"
    rent_display = format_currency(row.get("negotiated_rent") or row.get("asking_rent"))

    with grid_cols[col_idx]:
        if is_front:
            st.markdown(
                f"""
                <div class="property-card">
                    <div>
                        <div class="prop-title">{row.get('address', 'Property')}</div>
                        <div class="prop-sub">Score: {row.get('match_score')} • {row.get('bed_bath_count', 'N/A')}</div>
                        <div class="prop-huge-val">{rent_display}</div>
                        <div class="prop-sub" style="margin-top:-10px;">Monthly Rent</div>
                    </div>
                    <div style="margin-top: 20px;">
                        <div class="prop-sub"><b>Parking:</b> {row.get('parking_available', 'N/A')}</div>
                        <div class="prop-sub"><b>Pets:</b> {row.get('pet_policy', 'N/A')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Flip to Broker Conversation", key=f"btn_front_{idx}"):
                st.session_state.card_states[listing_id] = "back"
                st.rerun()
        else:
            st.markdown(
                f"""
                <div class="property-card" style="background-color: #E8EAEF;">
                    <div>
                        <div class="prop-title">Confirmed with Broker</div>
                        <div class="prop-sub">{row.get('address', 'Property')}</div>
                        <div style="margin-top: 16px;">
                            <div class="prop-sub"><b>Available:</b> {row.get('available_from_date', 'Immediate')}</div>
                            <div class="prop-sub"><b>Concessions:</b> {row.get('concessions_granted', 'None')}</div>
                        </div>
                        <div style="margin-top: 16px;">
                            <div class="prop-sub" style="line-height: 1.4;"><b>Notes:</b><br>{row.get('landlord_notes', 'No notes recorded.')}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Flip to Flat Overview", key=f"btn_back_{idx}"):
                st.session_state.card_states[listing_id] = "front"
                st.rerun()