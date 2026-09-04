import pandas as pd
import streamlit as st

def render_metrics(df: pd.DataFrame):
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    
    total = len(df)
    tours = int(df["tour_confirmed"].sum()) if "tour_confirmed" in df.columns else 0
    conv = (tours / total * 100) if total > 0 else 0
    top_score = df['match_score'].max() if not df.empty else 0

    items = [
        (m1, "bg-mustard", "L", total, "Listings Prescreened"),
        (m2, "bg-slate", "T", tours, "Tours Secured"),
        (m3, "bg-orange", "%", f"{conv:.0f}%", "Conversion Rate"),
        (m4, "", "A", top_score, "Top Match Score")
    ]

    for col, bg, icon, val, label in items:
        style = 'background-color: #E7DED8;' if not bg else ''
        with col:
            st.markdown(f"""
                <div class="metric-container {bg}" style="{style}">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)