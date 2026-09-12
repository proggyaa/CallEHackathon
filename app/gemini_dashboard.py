# app/gemini_dashboard.py
import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

from app.core import data_handler, runner
from app.components import styling, states, filters, grids

def main():
    st.set_page_config(layout="wide", page_title="Flat Hunting Control Center")
    styling.render_css()
    
    # 1. Capture User Input & Events (Runs once)
    must_haves, negotiables, save_clicked, initiate_clicked = filters.render_renter_choice_input()

    if save_clicked:
        filters.save_prefs(must_haves, negotiables)
        st.success("Preferences saved successfully!")

    # 2. Chronological Calling Status Handler
    if initiate_clicked:
        filters.save_prefs(must_haves, negotiables)
        
        with st.status("Initiating Agent Calls...", expanded=True) as status:
            status_box = st.empty()
            last_logs = []
            
            try:
                for log_line in runner.trigger_batch_prescreen_stream():
                    last_logs.append(log_line)
                    if "Initiating CALL-E agent for target:" in log_line:
                        status_box.markdown(
                            f"""
                            <div style="
                                border: 1.5px solid #000000;
                                border-radius: 20px;
                                padding: 14px 24px;
                                text-align: center;
                                font-size: 18px;
                                font-weight: 500;
                                background-color: #FFFFFF;
                                margin: 16px 0;
                            ">
                                Calling <b>{log_line.split(':')[-1].strip()}</b>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                status.update(label="All Calls Completed!", state="complete", expanded=False)
                st.rerun()

            except Exception as e:
                status.update(label="Batch Prescreen Failed", state="error")
                st.error(f"Error details: {e}")
                if last_logs:
                    st.code("\n".join(last_logs[-10:]))

    # 3. Render Listing Grid (Pass live must_haves selection)
    df_raw = data_handler.load_data()
    if df_raw.empty:
        states.render_empty_state(
            "No Listings Populated", 
            "Configure your preferences above and click 'Initiate Calls' to execute agent screening."
        )
        st.stop()

    grids.render_property_grid(df_raw, must_haves=must_haves)

if __name__ == "__main__":
    main()