# app/components/grids.py
import json
import os
import pandas as pd
import streamlit as st
from app.core import scoring

def get_status_label(color_code: str) -> str:
    """Returns the text badge label based on the calculated score color."""
    if color_code == "#A4CE8B":
        return "MATCHED"
    elif color_code == "#FFBE91":
        return "NEGOTIABLE"
    elif color_code == "#9E3B3B":
        return "REJECTED"
    return "UNSCREENED"

def render_property_grid(df: pd.DataFrame, must_haves: list | None = None):
    active_must_haves: list = must_haves if must_haves is not None else []
    
    # Load stored call results
    call_results_map = {}
    if os.path.exists("batch_results.json"):
        try:
            with open("batch_results.json", "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    call_results_map = {item.get("address", "").strip(): item.get("result", {}) for item in data}
        except Exception:
            pass

    if "card_states" not in st.session_state: 
        st.session_state.card_states = {}

    grid_cols = st.columns(3, gap="large")

    for idx, (_, row) in enumerate(df.iterrows()):
        col_idx = idx % 3
        l_id = str(row.get("address", f"listing_{idx}"))
        st.session_state.card_states.setdefault(l_id, "front")
        
        is_front = st.session_state.card_states[l_id] == "front"

        # Compute dynamic card color based on active must_haves selection
        address = str(row.get("address", "")).strip()
        call_res = row.get("call_result") or call_results_map.get(address) or {}
        bg_color = scoring.evaluate_listing_color(call_res, active_must_haves)
        
        # Get status label text (MATCHED, NEGOTIABLE, REJECTED)
        status_label = get_status_label(bg_color)

        # Text contrast logic for dark red card (#9E3B3B)
        is_dark_bg = bg_color == "#9E3B3B"
        text_color = "#FFFFFF" if is_dark_bg else "#000000"
        subtext_color = "rgba(255, 255, 255, 0.85)" if is_dark_bg else "#444444"
        badge_bg = "rgba(255, 255, 255, 0.25)" if is_dark_bg else "rgba(0, 0, 0, 0.1)"

        with grid_cols[col_idx]:
            card_key = f"property_card_{idx}"
            
            # Dynamically style each native Streamlit container by key
            st.markdown(f"""
                <style>
                div[class*="st-key-{card_key}"] {{
                    background-color: {bg_color} !important;
                    border-radius: 20px !important;
                    border: 1px solid rgba(0,0,0,0.08) !important;
                    padding: 20px 20px 20px 20px !important;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
                }}
                div[class*="st-key-{card_key}"] div.stButton > button {{
                    background-color: rgba(255, 255, 255, 0.6) !important;
                    border: 1px solid rgba(0, 0, 0, 0.1) !important;
                    color: #1E1E1E !important;
                    border-radius: 12px !important;
                    font-weight: 600 !important;
                    margin-top: 14px !important;
                }}
                div[class*="st-key-{card_key}"] div.stButton > button:hover {{
                    background-color: rgba(255, 255, 255, 0.85) !important;
                }}
                </style>
            """, unsafe_allow_html=True)

            with st.container(key=card_key):
                if is_front:
                    st.markdown(f"""
                        <div style="color: {text_color}; text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
                            <div style="
                                font-size: 11px; 
                                font-weight: 800; 
                                letter-spacing: 1px; 
                                padding: 3px 10px; 
                                border-radius: 20px; 
                                background-color: {badge_bg}; 
                                color: {text_color};
                                margin-bottom: 6px;
                            ">
                                {status_label}
                            </div>
                            <div>
                                <div style="font-size: 20px; font-weight: 700; margin-bottom: 6px; line-height: 1.2;">
                                    {row.get('address', 'Apartment Name')}
                                </div>
                                <div style="font-size: 15px; margin-bottom: 2px; font-weight: 500;">
                                    {row.get('broker_name', 'Broker Name')}
                                </div>
                                <div style="font-size: 14px; color: {subtext_color}; font-family: monospace;">
                                    {row.get('broker_contact', 'Broker Contact')}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Flip On Tap", key=f"btn_f_{idx}", use_container_width=True):
                        st.session_state.card_states[l_id] = "back"
                        st.rerun()
                else:
                    st.markdown(f"""
                        <div style="color: {text_color}; min-height: 150px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="text-align: center; margin-bottom: 6px;">
                                <span style="
                                    font-size: 11px; 
                                    font-weight: 800; 
                                    letter-spacing: 1px; 
                                    padding: 3px 10px; 
                                    border-radius: 20px; 
                                    background-color: {badge_bg}; 
                                    color: {text_color};
                                ">
                                    {status_label}
                                </span>
                            </div>
                            <div>
                                <div style="margin-bottom: 6px;">
                                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase;">Has</div>
                                    <div style="font-size: 13px; color: {subtext_color};">{', '.join(call_res.get('confirmed_amenities', [])) or row.get('renter_preferences', 'N/A')}</div>
                                </div>
                                <div style="margin-bottom: 6px;">
                                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase;">Negotiable</div>
                                    <div style="font-size: 13px; color: {subtext_color};">{', '.join(call_res.get('negotiable_amenities', [])) or row.get('broker_asks', 'N/A')}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase;">Non Negotiable</div>
                                    <div style="font-size: 13px; color: {subtext_color};">{', '.join(call_res.get('rejected_amenities', [])) or row.get('non_negotiables', 'N/A')}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Flip On Tap", key=f"btn_b_{idx}", use_container_width=True):
                        st.session_state.card_states[l_id] = "front"
                        st.rerun()