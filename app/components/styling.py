import streamlit as st

def render_css():
    st.markdown("""
        <style>
        .stApp { background-color: #F8F9FA; font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif; color: #000000; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background-color: #FFFFFF !important; border-radius: 30px !important; border: 1px solid #E0E0E0 !important; box-shadow: none !important; }
        label[data-testid="stWidgetLabel"] { font-size: 12px !important; font-weight: 500 !important; color: #000000 !important; margin-left: 8px !important; }
        .metric-container { border-radius: 24px; padding: 24px; color: #000000; min-height: 140px; display: flex; flex-direction: column; justify-content: flex-end; position: relative; }
        .metric-icon { position: absolute; top: 20px; left: 20px; background: #FFFFFF; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }
        .bg-mustard { background-color: #D2BE7B; }
        .bg-slate { background-color: #8DABBC; }
        .bg-orange { background-color: #F26531; }
        .metric-value { font-size: 36px; font-weight: 500; line-height: 1.1; margin-bottom: 4px; letter-spacing: -1px; }
        .metric-label { font-size: 13px; font-weight: 400; opacity: 0.9; }
        .property-card { background-color: #F2F3F5; border-radius: 28px; padding: 28px; margin-bottom: 24px; min-height: 260px; display: flex; flex-direction: column; justify-content: space-between; }
        .prop-huge-val { font-size: 42px; font-weight: 500; letter-spacing: -1.5px; line-height: 1; margin: 16px 0; }
        .prop-title { font-size: 18px; font-weight: 500; }
        .prop-sub { font-size: 13px; color: #555; }
        div.stButton > button { background-color: #FFFFFF !important; color: #000000 !important; border: 1px solid #E0E0E0 !important; border-radius: 30px !important; font-size: 13px !important; font-weight: 500 !important; height: 36px !important; width: fit-content !important; padding: 0 20px !important; }
        div.stButton > button:hover { background-color: #EFEFEF !important; }
        </style>
    """, unsafe_allow_html=True)