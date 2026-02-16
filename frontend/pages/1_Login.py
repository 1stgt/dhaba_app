import streamlit as st
from api_client import APIClient
import time

st.set_page_config(page_title="Vendor Login", page_icon="🔐")

st.title("🔐 Vendor Login")

if "token" in st.session_state and st.session_state.token:
    st.success("You are already logged in.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/2_Dashboard.py")
else:
    email = st.text_input("Email", placeholder="admin@dhaba.com")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        with st.spinner("Authenticating..."):
            result = APIClient.login(email, password)
            
            if "access_token" in result:
                st.session_state.token = result["access_token"]
                st.success("Login Successful!")
                time.sleep(1)
                st.switch_page("pages/2_Dashboard.py")
            else:
                st.error(result.get("error", "Login failed"))
