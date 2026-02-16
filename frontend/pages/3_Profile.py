import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import APIClient

st.set_page_config(page_title="Stall Profile", page_icon="🏪")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")

st.title("🏪 Stall Profile")

if st.button("⬅ Back to Dashboard"):
    st.switch_page("pages/2_Dashboard.py")

vendor = APIClient.get_vendor_profile()

if vendor:
    with st.form("profile_form"):
        stall_name = st.text_input("Stall Name", value=vendor.get("stall_name", ""))
        owner_name = st.text_input("Owner Name", value=vendor.get("owner_name", ""))
        phone = st.text_input("Phone Number", value=vendor.get("phone_number", ""))
        city = st.text_input("City", value=vendor.get("city", ""))
        upi_id = st.text_input("UPI ID", value=vendor.get("upi_id") or "")
        
        submitted = st.form_submit_button("Update Profile")
        
        if submitted:
            update_data = {
                "stall_name": stall_name,
                "owner_name": owner_name,
                "phone_number": phone,
                "city": city,
                "upi_id": upi_id
            }
            with st.spinner("Updating..."):
                response = APIClient.update_profile(update_data)
                if response and "id" in response:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Failed to update profile.")
