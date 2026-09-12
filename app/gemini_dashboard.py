import sys
from pathlib import Path
import streamlit as st

# Ensure Python can find your 'app' modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core import data_handler
from app.components import styling, states, filters, grids

def main():
    st.set_page_config(layout="wide", page_title="Flat Hunting Control Center")
    styling.render_css()
    
    df_raw = data_handler.load_data()
    if df_raw.empty:
        states.render_empty_state("System Halted", "No listings found. Execute prescreen_runner.py to populate data.")
        st.stop()

    # Renter Choice Input Card
    must_haves, negotiables = filters.render_renter_choice_input()

    # Pass raw listings directly to grid view
    grids.render_property_grid(df_raw)

if __name__ == "__main__":
    main()