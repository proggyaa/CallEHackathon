import sys
from pathlib import Path
import streamlit as st

# Ensure Python can find your 'app' modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core import data_handler, scoring
from app.components import styling, states, filters, metrics, grids

def main():
    st.set_page_config(layout="wide", page_title="Flat Hunting Control Center")
    styling.render_css()
    
    df_raw = data_handler.load_data()
    if df_raw.empty:
        states.render_empty_state("System Halted", "No listings found. Execute prescreen_runner.py to populate data.")
        st.stop()

    prefs, max_budget = filters.render_filters()
    df_scored = scoring.process_listings(df_raw, prefs, max_budget)

    if df_scored.empty:
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        states.render_empty_state("Zero Matches", "The current parameters yielded no results. Relax constraints to view listings.", bg_color="#E7DED8", border="none")
        st.stop()

    metrics.render_metrics(df_scored)
    grids.render_property_grid(df_scored)

if __name__ == "__main__":
    main()