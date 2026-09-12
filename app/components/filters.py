# app/components/filters.py
import json
import os
import streamlit as st

PREFS_FILE = "config/renter_prefs.json"

def load_prefs() -> dict:
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, "r") as f:
            return json.load(f)
    return {"must_haves": [], "negotiables": []}

def save_prefs(must_haves: list, negotiables: list) -> None:
    os.makedirs(os.path.dirname(PREFS_FILE), exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump({"must_haves": must_haves, "negotiables": negotiables}, f)

def render_renter_choice_input() -> tuple[list, list, bool, bool]:
    """
    Renders the preferences card.
    Returns: (must_haves, negotiables, save_clicked, initiate_clicked)
    """
    st.markdown("""
        <style>
        .renter-choice-card {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 28px;
            padding: 32px;
            max-width: 600px;
            margin: 0 auto 32px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        .renter-choice-title {
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 24px;
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)

    options = [
        "Parking Available", "Pet Policy Allowed", "Furnished", 
        "In-Unit Laundry", "Dishwasher", "Rent Concessions", "Immediate Availability"
    ]

    prefs = load_prefs()

    with st.container():
        st.markdown('<div class="renter-choice-card"><div class="renter-choice-title">Renter Choice Input</div>', unsafe_allow_html=True)
        
        must_haves = st.multiselect(
            "Must Haves",
            options=options,
            default=prefs.get("must_haves", []),
            placeholder="Select Must Haves...",
            key="must_haves_input"
        )

        negotiables = st.multiselect(
            "Negotiables",
            options=options,
            default=prefs.get("negotiables", []),
            placeholder="Select Negotiables...",
            key="negotiables_input"
        )
        
        st.write("")
        col1, col2 = st.columns(2)
        
        with col1:
            save_clicked = st.button("Save Preferences", key="save_prefs_btn", use_container_width=True)
            
        with col2:
            initiate_clicked = st.button("Initiate Calls", key="initiate_calls_btn", type="primary", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    return must_haves, negotiables, save_clicked, initiate_clicked