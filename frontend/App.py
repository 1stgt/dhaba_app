import streamlit as st

st.set_page_config(
    page_title="Dhaba App - Vendor",
    page_icon="🍛",
    layout="centered"
)

st.title("🍛 Dhaba App Vendor Portal")

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    st.info("Please log in to manage your stall.")
    st.page_link("pages/1_Login.py", label="Go to Login", icon="🔐")
else:
    st.success("You are logged in!")
    st.page_link("pages/2_Dashboard.py", label="Go to Dashboard", icon="📊")
    
st.divider()
st.caption("Dhaba App - Vendor Onboarding System v1.0")
