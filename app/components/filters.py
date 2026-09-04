import streamlit as st
from app.core.data_handler import PREF_OPTIONS

def render_filters() -> tuple[dict, int]:
    st.markdown("<div style='font-size: 20px; font-weight: 500; letter-spacing: -0.5px; margin-bottom: 12px;'>Parameters</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        pet = st.selectbox("Pet Policy", PREF_OPTIONS, index=0)
        park = st.selectbox("Parking", PREF_OPTIONS, index=0)
    with c2:
        furnish = st.selectbox("Furnished", PREF_OPTIONS, index=0)
        laundry = st.selectbox("Laundry", PREF_OPTIONS, index=0)
    with c3:
        dish = st.selectbox("Dishwasher", PREF_OPTIONS, index=0)
    with c4:
        budget = st.number_input("Max Rent ($)", value=3000, step=100)

    prefs = {"pet_policy": pet, "parking_available": park, "furnishing_status": furnish, "laundry": laundry, "dishwasher": dish}
    return prefs, budget