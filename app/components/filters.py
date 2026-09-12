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
        @import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');
        
        .finding-nemo-card {
            background-color: #FFFFFF;
            border: 2px solid #1E1E1E;
            border-radius: 28px;
            padding: 36px;
            max-width: 750px;
            margin: 0 auto 32px auto;
            box-shadow: 2px 3px 0px #1E1E1E;
        }
        .nemo-title {
            font-family: 'Architects Daughter', cursive, sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #111111;
            margin-bottom: 16px;
        }
        .nemo-subtitle {
            font-family: 'Architects Daughter', cursive, sans-serif;
            font-size: 20px;
            color: #222222;
            line-height: 1.5;
            margin-bottom: 24px;
        }

        /* Must Haves Tag Styling - Red */
        div[class*="st-key-must_haves_wrap"] div[data-baseweb="tag"] {
            background-color: #FF4D4D !important;
            color: #FFFFFF !important;
        }
        div[class*="st-key-must_haves_wrap"] div[data-baseweb="tag"] span {
            color: #FFFFFF !important;
        }
        div[class*="st-key-must_haves_wrap"] div[data-baseweb="tag"] svg {
            fill: #FFFFFF !important;
        }

        /* Negotiables Tag Styling - #ADFF2F Green */
        div[class*="st-key-negotiables_wrap"] div[data-baseweb="tag"] {
            background-color: #ADFF2F !important;
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

    st.markdown("""
        <div class="finding-nemo-card">
            <div class="nemo-title">Welcome To FindingNemo</div>
            <div class="nemo-subtitle">
                Let our agent call apartment listing on your behalf<br>
                Just tell us your requriements and relax :)
            </div>
    """, unsafe_allow_html=True)
    
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
    col1, col2 = st.columns(2)
    
    with col1:
        save_clicked = st.button("Save Preferences", key="save_prefs_btn", use_container_width=True)
        
    with col2:
        initiate_clicked = st.button("Initiate Calls", key="initiate_calls_btn", type="primary", use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    return must_haves, negotiables, save_clicked, initiate_clicked