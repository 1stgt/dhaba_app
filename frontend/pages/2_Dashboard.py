import streamlit as st
import sys
import os

# Add parent directory to path to import api_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import APIClient

st.set_page_config(page_title="Vendor Dashboard", page_icon="📊")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")

st.title("📊 Vendor Dashboard")

vendor = APIClient.get_vendor_profile()

if vendor:
    st.subheader(f"Welcome, {vendor.get('owner_name', 'Vendor')}! 👋")
    st.caption(f"Stall: {vendor.get('stall_name')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏪 Update Profile", use_container_width=True):
            st.switch_page("pages/3_Profile.py")
            
    with col2:
        if st.button("📜 Manage Menu", use_container_width=True):
            st.switch_page("pages/4_Menu.py")
            
    with col3:
        if st.button("🏁 View QR Code", use_container_width=True):
            st.switch_page("pages/5_QR_Code.py")
            
else:
    st.error("Failed to fetch profile. Please login again.")
