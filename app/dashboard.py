"""Streamlit dashboard for flat prescreening leads and viewing schedules."""

from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).parent.parent / "listings.db"

st.set_page_config(page_title="Flat Hunting Control Center", layout="wide")
st.title("Flat Hunting Prescreener Dashboard")


def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM listings ORDER BY called_at DESC", conn
        )
    return df


df = load_data()

if df.empty:
    st.info(
        "No call records found. Run `prescreen_runner.py` to populate data."
    )
else:
    total_calls = len(df)
    tours_booked = int(df["tour_confirmed"].sum())
    confirmed_df = df[df["tour_confirmed"] == 1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Prescreened", total_calls)
    col2.metric("Tours Booked", tours_booked)
    col3.metric(
        "Conversion Rate",
        (
            f"{(tours_booked / total_calls * 100):.1f}%"
            if total_calls > 0
            else "0%"
        ),
    )

    st.markdown("---")

    st.subheader("Confirmed Viewing Schedule")
    if not confirmed_df.empty:
        schedule_cols = [
            "address",
            "phone",
            "agreed_monthly_rent",
            "tour_iso_time",
            "bed_bath_count",
            "landlord_notes",
        ]
        schedule_df = confirmed_df[schedule_cols].copy()
        schedule_df.columns = [
            "Address",
            "Phone",
            "Rent",
            "Tour Time",
            "Layout",
            "Notes",
        ]
        st.dataframe(schedule_df, use_container_width=True)
    else:
        st.write("No confirmed tours scheduled yet.")

    st.markdown("---")

    st.subheader("Property Features & Listing Details")
    property_cols = [
        "address",
        "bed_bath_count",
        "agreed_monthly_rent",
        "security_deposit",
        "available_from_date",
        "pet_policy",
        "furnishing_status",
        "parking_available",
        "concessions",
        "recommended_action",
    ]
    st.dataframe(df[property_cols], use_container_width=True)