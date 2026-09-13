import streamlit as st

def render_empty_state(title: str, message: str, bg_color: str = "#FFFFFF", border: str = "2px solid #000000"):
    st.markdown(f"""
        <div style="background-color:{bg_color}; border:{border}; border-radius:24px; padding:24px;">
            <div style="font-size:24px; font-weight:500; letter-spacing:-1px; margin-bottom:8px;">{title}</div>
            <div style="font-size:14px; color:#555;">{message}</div>
        </div>
    """, unsafe_allow_html=True)