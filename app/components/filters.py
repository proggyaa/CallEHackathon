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

def render_header_banner():
    """Renders the banner logo outside at the top, smaller, centered, and pushed upwards."""
    st.markdown("""
        <style>
        /* Pull the top image container up */
        div[class*="st-key-top_banner_container"] {
            margin-top: -100px !important;
            margin-bottom: -15px !important;
            padding-top: 0px !important;
        }

        div[data-testid="stImage"] {
            margin-bottom: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container(key="top_banner_container"):
        col_l, col_img, col_r = st.columns([1.5, 3, 1.5])
        with col_img:
            st.image("assets/header_logo.png", use_container_width=True)

def render_renter_choice_input() -> tuple[list, list, bool, bool]:
    st.markdown("""
        <style>
        /* Elevated Main Wrapper Box with Organic Border & Soft Tinted Shadow */
        div[class*="st-key-main_elevated_card"] {
            background-color: #FFFDF9 !important;
            border-radius: 28px 24px 30px 22px !important;
            border: 2px solid #3A3226 !important;
            padding: 32px 32px !important;
            box-shadow: 4px 6px 0px #3A3226 !important;
            margin-top: 0px !important;
            margin-bottom: 30px !important;
        }

        /* Subheading Micro-copy */
        .header-subtitle {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 17px;
            font-weight: 500;
            color: #3A3226;
            line-height: 1.5;
            text-align: center;
            margin-top: 0px;
            margin-bottom: 24px;
        }

        /* Custom Coral-Red Chip Tags for Must Haves */
        div[class*="st-key-must_haves_wrap"] [data-baseweb="tag"] {
            background-color: #E8604C !important;
            border: 1.5px solid #3A3226 !important;
            border-radius: 12px 14px 10px 16px !important;
            transform: rotate(-0.8deg);
        }
        div[class*="st-key-must_haves_wrap"] [data-baseweb="tag"] * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Custom Muted Peach Chip Tags for Negotiables */
        div[class*="st-key-negotiables_wrap"] [data-baseweb="tag"] {
            background-color: #F7C59F !important;
            border: 1.5px solid #3A3226 !important;
            border-radius: 14px 10px 16px 12px !important;
            transform: rotate(0.8deg);
        }
        div[class*="st-key-negotiables_wrap"] [data-baseweb="tag"] * {
            color: #3A2412 !important;
            fill: #3A2412 !important;
            font-weight: 600 !important;
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

    # Subtitle Micro-copy inside the card top
    st.markdown("""
        <div class="header-subtitle">
            Let our agent call apartment listings on your behalf.<br>
            Just tell us your requirements and relax :)
        </div>
    """, unsafe_allow_html=True)

    # Input Fields
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