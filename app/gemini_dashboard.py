# app/gemini_dashboard.py
import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

from app.core import data_handler, runner
from app.components import styling, states, filters, grids

def main():
    st.set_page_config(layout="wide", page_title="NemoTheFinder Operations")
    
    # 1. Inject dark monospace ops CSS
    styling.render_css()
    
    # 2. Render choice inputs & filters
    must_haves, negotiables, save_clicked, initiate_clicked = filters.render_renter_choice_input()

    if save_clicked:
        filters.save_prefs(must_haves, negotiables)
        st.toast("Preferences saved to config/renter_prefs.json")

    if initiate_clicked:
        filters.save_prefs(must_haves, negotiables)
        with st.status("Dispatching Agent Calls...", expanded=True) as status:
            status_box = st.empty()
            last_logs = []
            try:
                for log_line in runner.trigger_batch_prescreen_stream():
                    last_logs.append(log_line)
                    if "Initiating CALL-E agent for target:" in log_line:
                        status_box.markdown(
                            f"""
                            <div style="border: 1px solid #E8B04B; border-radius: 6px; padding: 10px 16px; text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 13px; background-color: #1A1A1D; color: #EDEDED; margin: 8px 0;">
                                [DISPATCH] Target: <strong>{log_line.split(':')[-1].strip()}</strong>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                status.update(label="Batch Execution Complete", state="complete", expanded=False)
                st.rerun()
            except Exception as e:
                status.update(label="Batch Prescreen Error", state="error")
                st.error(f"Details: {e}")
                if last_logs:
                    st.code("\n".join(last_logs[-10:]))

    # 3. Render Listing Grid
    df_raw = data_handler.load_data()
    if df_raw.empty:
        states.render_empty_state(
            "No Listings Loaded", 
            "Execute database seeding or initiate call batch."
        )
        st.stop()

    grids.render_property_grid(df_raw, must_haves=must_haves)

if __name__ == "__main__":
    main()