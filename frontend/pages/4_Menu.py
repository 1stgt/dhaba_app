import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import APIClient

st.set_page_config(page_title="Menu Manager", page_icon="📜")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")

st.title("📜 Menu Manager")

if st.button("⬅ Back to Dashboard"):
    st.switch_page("pages/2_Dashboard.py")

# --- Add New Item ---
with st.expander("➕ Add New Item", expanded=False):
    with st.form("add_item_form", clear_on_submit=True):
        new_name = st.text_input("Item Name")
        new_desc = st.text_area("Description")
        new_price = st.number_input("Price (₹)", min_value=0, step=1)
        
        added = st.form_submit_button("Add Item")
        if added:
            if new_name and new_price:
                data = {
                    "name": new_name,
                    "description": new_desc,
                    "price": int(new_price),
                    "is_available": True
                }
                res = APIClient.add_menu_item(data)
                if res and "id" in res:
                    st.success("Item added!")
                    st.rerun()
                else:
                    st.error("Failed to add item.")
            else:
                st.error("Name and Price are required.")

st.divider()

# --- List Items ---
st.subheader("Current Menu")
items = APIClient.get_menu_items()

if not items:
    st.info("No items in menu yet.")
else:
    for item in items:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"**{item['name']}**")
                st.caption(item.get('description', ''))
            with c2:
                st.markdown(f"₹{item['price']}")
            with c3:
                is_active = item['is_available']
                if st.button("Disable" if is_active else "Enable", key=f"toggle_{item['id']}"):
                    APIClient.update_menu_item(item['id'], {"is_available": not is_active})
                    st.rerun()
