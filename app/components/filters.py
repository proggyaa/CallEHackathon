import streamlit as st

def render_renter_choice_input():
    st.markdown("""
        <style>
        .renter-choice-card {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 28px;
            padding: 32px;
            max-width: 500px;
            margin: 0 auto 32px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        .renter-choice-title {
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 24px;
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)

    options = [
        "Parking Available",
        "Pet Policy Allowed",
        "Furnished",
        "In-Unit Laundry",
        "Dishwasher",
        "Rent Concessions",
        "Immediate Availability"
    ]

    with st.container():
        st.markdown('<div class="renter-choice-card"><div class="renter-choice-title">Renter Choice Input</div>', unsafe_allow_html=True)
        
        must_haves = st.multiselect(
            "Must Haves",
            options=options,
            placeholder="Select Must Haves...",
            key="must_haves_input"
        )

        negotiables = st.multiselect(
            "Negotiables",
            options=options,
            placeholder="Select Negotiables...",
            key="negotiables_input"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

    return must_haves, negotiables
