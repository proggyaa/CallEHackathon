import pandas as pd
import streamlit as st
from app.core.data_handler import format_currency

def render_property_grid(df: pd.DataFrame):
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    if "card_states" not in st.session_state: st.session_state.card_states = {}
    
    grid_cols = st.columns(3, gap="large")

    for idx, (_, row) in enumerate(df.iterrows()):
        col_idx = idx % 3
        l_id = str(row.get("address", f"listing_{idx}"))
        st.session_state.card_states.setdefault(l_id, "front")
        
        is_front = st.session_state.card_states[l_id] == "front"
        rent = format_currency(row.get("negotiated_rent") or row.get("asking_rent"))

        with grid_cols[col_idx]:
            if is_front:
                st.markdown(f"""
                    <div class="property-card">
                        <div>
                            <div class="prop-title">{row.get('address', 'Property')}</div>
                            <div class="prop-sub">Score: {row.get('match_score')} • {row.get('bed_bath_count', 'N/A')}</div>
                            <div class="prop-huge-val">{rent}</div>
                            <div class="prop-sub" style="margin-top:-10px;">Monthly Rent</div>
                        </div>
                        <div style="margin-top: 20px;">
                            <div class="prop-sub"><b>Parking:</b> {row.get('parking_available', 'N/A')}</div>
                            <div class="prop-sub"><b>Pets:</b> {row.get('pet_policy', 'N/A')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Flip to Broker Conversation", key=f"btn_f_{idx}"):
                    st.session_state.card_states[l_id] = "back"
                    st.rerun()
            else:
                st.markdown(f"""
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
                if st.button("Flip to Flat Overview", key=f"btn_b_{idx}"):
                    st.session_state.card_states[l_id] = "front"
                    st.rerun()