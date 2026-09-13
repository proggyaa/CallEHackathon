# app/components/styling.py
import streamlit as st

def render_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        /* Outer Canvas Background with Warm Paper Palette & Grain texture */
        .stApp, 
        [data-testid="stAppViewContainer"], 
        header[data-testid="stHeader"], 
        .main {
            background-color: #F5EDE4 !important;
            font-family: 'Space Grotesk', sans-serif !important;
            color: #3A3226 !important;
        }

        /* Typography */
        h1, h2, h3, .header-title, .prop-title { 
            font-family: 'Fraunces', serif !important; 
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
            color: #3A3226 !important;
        }

        /* Tactile Button Styling - Slight scale down on click */
        div.stButton > button { 
            font-family: 'Space Grotesk', sans-serif !important;
            background-color: #FFFDF9 !important; 
            color: #3A3226 !important; 
            border: 2px solid #3A3226 !important; 
            border-radius: 14px 18px 12px 16px !important; 
            font-size: 14px !important; 
            font-weight: 700 !important; 
            height: 44px !important; 
            padding: 0 24px !important; 
            box-shadow: 2px 3px 0px #3A3226 !important;
            transition: all 0.15s ease-in-out !important;
        }
        
        div.stButton > button:hover { 
            background-color: #F5EDE4 !important; 
            transform: translateY(-1px) !important;
            box-shadow: 3px 4px 0px #3A3226 !important;
        }

        div.stButton > button:active { 
            transform: translateY(2px) !important;
            box-shadow: 0px 1px 0px #3A3226 !important;
        }

        /* Initiate Calls Primary Button */
        div.stButton > button[kind="primary"] {
            background-color: #E8604C !important;
            color: #FFFFFF !important;
            border: 2px solid #3A3226 !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background-color: #D4503C !important;
            color: #FFFFFF !important;
        }

        /* Custom Input Boxes Styling */
        div[data-baseweb="select"] > div { 
            background-color: #FFFDF9 !important; 
            border-radius: 14px 12px 16px 14px !important; 
            border: 2px solid #3A3226 !important; 
            box-shadow: 2px 2px 0px rgba(58, 50, 38, 0.15) !important; 
        }
        
        label[data-testid="stWidgetLabel"] { 
            font-family: 'Fraunces', serif !important;
            font-size: 16px !important; 
            font-weight: 700 !important; 
            color: #3A3226 !important; 
        }
        </style>
    """, unsafe_allow_html=True)