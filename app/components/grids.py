# app/components/grids.py
import json
import os
import pandas as pd
import streamlit as st
from app.core import scoring

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

        # Compute dynamic card color using scoring module
        address = str(row.get("address", "")).strip()
        call_res = row.get("call_result") or call_results_map.get(address) or {}
        bg_color = scoring.evaluate_listing_color(call_res, active_must_haves)
        text_color = "#FFFFFF" if bg_color == "#9E3B3B" else "#000000"
        subtext_color = "#DDD" if bg_color == "#9E3B3B" else "#444"

        with grid_cols[col_idx]:
            if is_front:
                st.markdown(f"""
                    <div class="property-card" style="justify-content: center; align-items: center; text-align: center; background-color: {bg_color}; color: {text_color}; border: 1px solid #E0E0E0; border-radius: 16px; padding: 20px;">
                        <div>
                            <div class="prop-title" style="font-size: 22px; font-weight: 600; margin-bottom: 8px;">
                                {row.get('address', 'Apartment Name')}
                            </div>
                            <div class="prop-sub" style="font-size: 15px; margin-bottom: 4px;">
                                {row.get('broker_name', 'Broker Name')}
                            </div>
                            <div class="prop-sub" style="font-size: 14px; color: {subtext_color};">
                                {row.get('broker_contact', 'Broker Contact')}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Flip On Tap", key=f"btn_f_{idx}"):
                    st.session_state.card_states[l_id] = "back"
                    st.rerun()
            else:
                st.markdown(f"""
                    <div class="property-card" style="background-color: {bg_color}; color: {text_color}; border: 1px solid #E0E0E0; border-radius: 16px; padding: 20px;">
                        <div>
                            <div style="margin-bottom: 16px;">
                                <div style="font-size: 14px; font-weight: 600;">Confirmed Amenities</div>
                                <div class="prop-sub" style="color: {subtext_color};">{', '.join(call_res.get('confirmed_amenities', [])) or 'None'}</div>
                            </div>
                            <div style="margin-bottom: 16px;">
                                <div style="font-size: 14px; font-weight: 600;">Negotiable</div>
                                <div class="prop-sub" style="color: {subtext_color};">{', '.join(call_res.get('negotiable_amenities', [])) or 'None'}</div>
                            </div>
                            <div>
                                <div style="font-size: 14px; font-weight: 600;">Non Negotiable</div>
                                <div class="prop-sub" style="color: {subtext_color};">{', '.join(call_res.get('rejected_amenities', [])) or 'None'}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Flip On Tap", key=f"btn_b_{idx}"):
                    st.session_state.card_states[l_id] = "front"
                    st.rerun()