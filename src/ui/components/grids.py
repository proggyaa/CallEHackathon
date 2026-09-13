# app/components/grids.py
import json
from pathlib import Path
import pandas as pd
import streamlit as st
from src.domain import scoring

PROJECT_ROOT = Path(__file__).parents[3]

def get_status_palette(color_code: str) -> tuple[str, str, str, str]:
    """Returns (bg_color, text_color, subtext_color, badge_bg) mapped to earthy paper palette."""
    if color_code == "#A4CE8B": # Matched
        return "#A3C997", "#1E261B", "#384A33", "rgba(255, 255, 255, 0.55)"
    elif color_code == "#FFBE91": # Negotiable
        return "#F7C59F", "#3A2412", "#593B22", "rgba(255, 255, 255, 0.55)"
    elif color_code == "#9E3B3B": # Rejected
        return "#B85B5B", "#FFFFFF", "rgba(255, 255, 255, 0.9)", "rgba(0, 0, 0, 0.2)"
    else: # Default/Unscreened
        return "#E2D9D5", "#3A3226", "#544D47", "rgba(255, 255, 255, 0.6)"

def get_status_label(color_code: str) -> str:
    if color_code == "#A4CE8B":
        return "MATCHED"
    elif color_code == "#FFBE91":
        return "NEGOTIABLE"
    elif color_code == "#9E3B3B":
        return "REJECTED"
    return "UNSCREENED"

def render_property_grid(df: pd.DataFrame, must_haves: list | None = None):
    active_must_haves: list = must_haves if must_haves is not None else []
    
    call_results_map = {}
    results_file = PROJECT_ROOT / "data" / "raw" / "batch_results.json"
    if results_file.exists():
        try:
            with open(results_file, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    call_results_map = {item.get("address", "").strip(): item.get("result", {}) for item in data}
        except Exception:
            pass

    if "card_states" not in st.session_state: 
        st.session_state.card_states = {}

    grid_cols = st.columns(3, gap="large")

    # Rotation angles for slight imperfect layout
    rotations = [-1.0, 0.8, -0.6, 1.2, -0.7, 0.9]

    for idx, (_, row) in enumerate(df.iterrows()):
        col_idx = idx % 3
        l_id = str(row.get("address", f"listing_{idx}"))
        st.session_state.card_states.setdefault(l_id, "front")
        
        is_front = st.session_state.card_states[l_id] == "front"

        address = str(row.get("address", "")).strip()
        call_res = row.get("call_result") or call_results_map.get(address) or {}
        raw_color_code = scoring.evaluate_listing_color(call_res, active_must_haves)
        
        bg_color, text_color, subtext_color, badge_bg = get_status_palette(raw_color_code)
        status_label = get_status_label(raw_color_code)
        card_rotation = rotations[idx % len(rotations)]

        with grid_cols[col_idx]:
            card_key = f"property_card_{idx}"
            
            st.markdown(f"""
                <style>
                div[class*="st-key-{card_key}"] {{
                    background-color: {bg_color} !important;
                    border-radius: 22px 18px 24px 20px !important;
                    border: 2px solid #3A3226 !important;
                    padding: 24px !important;
                    box-shadow: 3px 5px 0px #3A3226 !important;
                    transform: rotate({card_rotation}deg);
                    transition: transform 0.2s ease;
                }}
                div[class*="st-key-{card_key}"]:hover {{
                    transform: rotate(0deg) translateY(-2px);
                }}
                div[class*="st-key-{card_key}"] div.stButton > button {{
                    background-color: {badge_bg} !important;
                    border: 1.5px solid #3A3226 !important;
                    color: {text_color} !important;
                    border-radius: 14px !important;
                    font-weight: 700 !important;
                    margin-top: 14px !important;
                    box-shadow: 2px 2px 0px #3A3226 !important;
                }}
                </style>
            """, unsafe_allow_html=True)

            with st.container(key=card_key):
                if is_front:
                    st.markdown(f"""
                        <div style="color: {text_color}; text-align: center; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
                            <div style="
                                font-size: 11px; 
                                font-weight: 800; 
                                letter-spacing: 1.5px; 
                                padding: 4px 14px; 
                                border-radius: 16px; 
                                background-color: {badge_bg}; 
                                border: 1px solid #3A3226;
                                color: {text_color};
                                margin-bottom: 8px;
                            ">
                                {status_label}
                            </div>
                            <div>
                                <div style="font-family: 'Fraunces', serif; font-size: 20px; font-weight: 700; margin-bottom: 6px; line-height: 1.2;">
                                    {row.get('address', 'Apartment Name')}
                                </div>
                                <div style="font-size: 15px; margin-bottom: 2px; font-weight: 600;">
                                    {row.get('broker_name', 'Broker Name')}
                                </div>
                                <div style="font-size: 13px; color: {subtext_color}; font-family: monospace;">
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
                        <div style="color: {text_color}; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="text-align: center; margin-bottom: 6px;">
                                <span style="
                                    font-size: 11px; 
                                    font-weight: 800; 
                                    letter-spacing: 1.5px; 
                                    padding: 4px 14px; 
                                    border-radius: 16px; 
                                    background-color: {badge_bg}; 
                                    border: 1px solid #3A3226;
                                    color: {text_color};
                                ">
                                    {status_label}
                                </span>
                            </div>
                            <div style="font-size: 13px;">
                                <div style="margin-bottom: 6px;">
                                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase;">Has</div>
                                    <div style="color: {subtext_color}; font-weight: 500;">{', '.join(call_res.get('confirmed_amenities', [])) or row.get('renter_preferences', 'N/A')}</div>
                                </div>
                                <div style="margin-bottom: 6px;">
                                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase;">Negotiable</div>
                                    <div style="color: {subtext_color}; font-weight: 500;">{', '.join(call_res.get('negotiable_amenities', [])) or row.get('broker_asks', 'N/A')}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase;">Non Negotiable</div>
                                    <div style="color: {subtext_color}; font-weight: 500;">{', '.join(call_res.get('rejected_amenities', [])) or row.get('non_negotiables', 'N/A')}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Flip On Tap", key=f"btn_b_{idx}", use_container_width=True):
                        st.session_state.card_states[l_id] = "front"
                        st.rerun()