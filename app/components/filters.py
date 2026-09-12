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
    st.markdown("""
        <style>
        /* Must Haves Tag Styling - Red */
        div[class*="st-key-must_haves_wrap"] div[data-baseweb="tag"] {
            background-color: #FF4D4D !important;
            color: #FFFFFF !important;
            border-radius: 12px !important;
        }
        div[class*="st-key-must_haves_wrap"] div[data-baseweb="tag"] span {
            color: #FFFFFF !important;
        }
        div[class*="st-key-must_haves_wrap"] div[data-baseweb="tag"] svg {
            fill: #FFFFFF !important;
        }

        /* Negotiables Tag Styling - Green */
        div[class*="st-key-negotiables_wrap"] div[data-baseweb="tag"] {
            background-color: #ADFF2F !important;
            border-radius: 12px !important;
        }
        div[class*="st-key-negotiables_wrap"] div[data-baseweb="tag"] span {
            color: #1E1E1E !important;
            font-weight: 600 !important;
        }
        div[class*="st-key-negotiables_wrap"] div[data-baseweb="tag"] svg {
            fill: #1E1E1E !important;
        }
        </style>
    """, unsafe_allow_html=True)

    all_options = [
        "Parking Available", "Pet Policy Allowed", "Furnished", 
        "In-Unit Laundry", "Dishwasher", "Rent Concessions", "Immediate Availability"
    ]

    prefs = load_prefs()

    if "must_haves_input" not in st.session_state:
        st.session_state["must_haves_input"] = prefs.get("must_haves", [])
    if "negotiables_input" not in st.session_state:
        st.session_state["negotiables_input"] = prefs.get("negotiables", [])

    must_have_options = [opt for opt in all_options if opt not in st.session_state["negotiables_input"]]
    negotiable_options = [opt for opt in all_options if opt not in st.session_state["must_haves_input"]]

    # Render Your Exact Image Banner Centered
    col_l, col_img, col_r = st.columns([1, 4, 1])
    with col_img:
        # Change filename extension to match your saved file (.png / .jpg)
        st.image("assets/header_logo.png", use_container_width=True)

    # Inputs
    with st.container(key="must_haves_wrap"):
        must_haves = st.multiselect(
            "Must Haves",
            options=must_have_options,
            placeholder="Select Must Haves...",
            key="must_haves_input"
        )

    with st.container(key="negotiables_wrap"):
        negotiables = st.multiselect(
            "Negotiables",
            options=negotiable_options,
            placeholder="Select Negotiables...",
            key="negotiables_input"
        )
    
    st.write("")

    # Action Buttons
    spacer_l, col1, col2, spacer_r = st.columns([2, 1, 1, 2])

    with col1:
        save_clicked = st.button("Save Preferences", key="save_prefs_btn", use_container_width=True)

    with col2:
        initiate_clicked = st.button("Initiate Calls", key="initiate_calls_btn", type="primary", use_container_width=True)

    return must_haves, negotiables, save_clicked, initiate_clicked