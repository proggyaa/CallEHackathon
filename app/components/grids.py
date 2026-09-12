import pandas as pd
import streamlit as st

def render_property_grid(df: pd.DataFrame):
    if "card_states" not in st.session_state: 
        st.session_state.card_states = {}
    
    grid_cols = st.columns(3, gap="large")

    for idx, (_, row) in enumerate(df.iterrows()):
        col_idx = idx % 3
        l_id = str(row.get("address", f"listing_{idx}"))
        st.session_state.card_states.setdefault(l_id, "front")
        
        is_front = st.session_state.card_states[l_id] == "front"

        with grid_cols[col_idx]:
            if is_front:
                st.markdown(f"""
                    <div class="property-card" style="justify-content: center; align-items: center; text-align: center;">
                        <div>
                            <div class="prop-title" style="font-size: 22px; font-weight: 600; margin-bottom: 8px;">
                                {row.get('address', 'Apartment Name')}
                            </div>
                            <div class="prop-sub" style="font-size: 15px; margin-bottom: 4px;">
                                {row.get('broker_name', 'Broker Name')}
                            </div>
                            <div class="prop-sub" style="font-size: 14px; color: #666;">
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
                    <div class="property-card" style="background-color: #FFFFFF; border: 1px solid #E0E0E0;">
                        <div>
                            <div style="margin-bottom: 16px;">
                                <div style="font-size: 14px; font-weight: 600;">What Apt has:</div>
                                <div class="prop-sub">Absolutely Has</div>
                                <div class="prop-sub" style="color: #444;">{row.get('renter_preferences', row.get('bed_bath_count', 'N/A'))}</div>
                            </div>
                            <div style="margin-bottom: 16px;">
                                <div style="font-size: 14px; font-weight: 600;">Negotiable</div>
                                <div class="prop-sub" style="color: #444;">{row.get('broker_asks', row.get('concessions_granted', 'N/A'))}</div>
                            </div>
                            <div>
                                <div style="font-size: 14px; font-weight: 600;">Non Negotiable</div>
                                <div class="prop-sub" style="color: #444;">{row.get('non_negotiables', row.get('pet_policy', 'N/A'))}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Flip On Tap", key=f"btn_b_{idx}"):
                    st.session_state.card_states[l_id] = "front"
                    st.rerun()