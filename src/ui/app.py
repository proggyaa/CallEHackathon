# app/dashboard.py
import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.database import data_handler
from src.ui import runner
from src.ui.components import styling, states, filters, grids

def main():
    st.set_page_config(layout="wide", page_title="Nemo The Finder")
    
    # 1. Inject global styling
    styling.render_css()

    # 2. Render Header Banner Image at Top (Outside Box)
    filters.render_header_banner()

    # 3. Elevated Main Box Wrapper
    with st.container(key="main_elevated_card"):
        must_haves, negotiables, save_clicked, initiate_clicked = filters.render_renter_choice_input()

        if save_clicked:
            filters.save_prefs(must_haves, negotiables)
            st.toast("Preferences saved to data/user/renter_prefs.json")

        if initiate_clicked:
            filters.save_prefs(must_haves, negotiables)
            with st.status("Nemo's on the phone...", expanded=True) as status:
                status_box = st.empty()
                last_logs = []
                try:
                    for log_line in runner.trigger_batch_prescreen_stream():
                        last_logs.append(log_line)
                        if "Initiating CALL-E agent for target:" in log_line:
                            target_name = log_line.split(':')[-1].strip()
                            status_box.markdown(
                                f"""
                                <div style="border: 2px solid #3A3226; border-radius: 12px; padding: 12px 18px; text-align: left; font-family: 'Space Grotesk', sans-serif; font-size: 14px; background-color: #F7C59F; color: #3A2412; margin: 8px 0; font-weight: 600;">
                                    📞 Nemo's on the phone with <strong>{target_name}</strong>...
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    status.update(label="All calls wrapped up!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    status.update(label="Nemo hit a snag while dialing", state="error")
                    st.error(f"Details: {e}")
                    if last_logs:
                        st.code("\n".join(last_logs[-10:]))

        st.markdown("<hr style='margin: 32px 0; border: none; border-top: 2px dashed rgba(58, 50, 38, 0.15);'>", unsafe_allow_html=True)

        # Render Property Grid
        df_raw = data_handler.load_data()
        if df_raw.empty:
            states.render_empty_state(
                "Nemo hasn't loaded any listings yet", 
                "Seed your database or hit initiate calls to get started."
            )
            st.stop()

        grids.render_property_grid(df_raw, must_haves=must_haves)

if __name__ == "__main__":
    main()