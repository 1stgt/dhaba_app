
import streamlit as st
import pandas as pd
from google_sheets_client import GoogleSheetsClient
import uuid
from datetime import datetime
import time

# --- Configuration ---
st.set_page_config(page_title="Dhaba App", page_icon="🥟", layout="wide")

# Initialize Client
if 'db_client' not in st.session_state:
    st.session_state.db_client = GoogleSheetsClient()

# Initialize Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(item, price):
    st.session_state.cart.append({"Item": item, "Price": price})
    st.toast(f"Added {item} to cart!")

def calculate_total():
    return sum(item['Price'] for item in st.session_state.cart)

def main():
    st.sidebar.title("🥟 Dhaba Manager")
    choice = st.sidebar.radio("Go to", ["Order Food", "Admin Dashboard", "QR Code"])

    if choice == "Order Food":
        st.title("Welcome to Our Dhaba! 🍛")
        
        # 1. Fetch Menu
        menu_df = st.session_state.db_client.get_menu()
        
        if not menu_df.empty:
            # Display Menu by Category
            categories = menu_df['Category'].unique()
            for category in categories:
                st.subheader(category)
                cat_items = menu_df[menu_df['Category'] == category]
                
                # Use columns for grid layout
                cols = st.columns(3)
                for index, row in cat_items.iterrows():
                    col = cols[index % 3]
                    with col:
                        # Displaying image (placeholder for now if link invalid or just text)
                        try:
                            st.image(row['Image'], use_column_width=True)
                        except:
                            st.text("No Image")
                            
                        st.markdown(f"**{row['Item']}**")
                        st.markdown(f"₹{row['Price']}")
                        if st.button(f"Add {row['Item']}", key=f"add_{index}"):
                            add_to_cart(row['Item'], row['Price'])
            
            st.divider()
            
            # 2. Cart Section
            st.subheader("🛒 Your Cart")
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.table(cart_df)
                
                total = calculate_total()
                st.write(f"**Total Bill: ₹{total}**")
                
                # Checkout Form
                with st.form("checkout_form"):
                    cust_name = st.text_input("Name / Table Number")
                    submitted = st.form_submit_button("Place Order")
                    
                    if submitted:
                        if cust_name:
                            order_id = str(uuid.uuid4())[:8]
                            order_data = {
                                "OrderID": order_id,
                                "CustomerName": cust_name,
                                "Items": ", ".join([item['Item'] for item in st.session_state.cart]),
                                "Total": total,
                                "Status": "Pending",
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            success = st.session_state.db_client.place_order(order_data)
                            
                            if success:
                                st.success(f"Order Placed! ID: {order_id}")
                                st.session_state.cart = [] # Clear cart
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Failed to place order. Try again.")
                        else:
                            st.warning("Please enter your name or table number.")
            else:
                st.info("Your cart is empty.")

    elif choice == "Admin Dashboard":
        st.title("👨‍🍳 Admin Dashboard")
        
        # Simple Pin/Password (Hardcoded for MVP)
        password = st.sidebar.text_input("Admin Password", type="password")
        if password == "admin123":
            st.success("Logged In")
            
            # 1. View Orders
            st.subheader("Active Orders")
            orders_df = st.session_state.db_client.get_orders()
            
            if not orders_df.empty:
                # Add filters?
                st.dataframe(orders_df)
                
                # Order Management
                st.markdown("### Update Status")
                order_ids = orders_df['OrderID'].tolist()
                selected_order = st.selectbox("Select Order ID", order_ids)
                new_status = st.selectbox("Set Status", ["Pending", "Preparing", "Ready", "Completed", "Cancelled"])
                
                if st.button("Update Status"):
                    st.session_state.db_client.update_order_status(selected_order, new_status)
                    st.success(f"Updated Order {selected_order} to {new_status}")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info("No orders yet.")
                
        else:
            if password:
                st.error("Incorrect Password")
                
    elif choice == "QR Code":
        st.title("📱 Scan to Order")
        
        import socket
        try:
            # unique way to get local IP on LAN
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "localhost"
            
        app_url = f"http://{local_ip}:8501"
        
        from utils import generate_qr_code
        qr_image = generate_qr_code(app_url)
        st.image(qr_image, caption=f"Scan to order from {app_url}", width=300)
        
        st.info(f"**Tip:** Connect your phone to the same Wi-Fi as this laptop to access the menu via {app_url}")
        st.warning("Note: If using Streamlit Cloud (deployed), this QR code will need the public URL instead.")

if __name__ == "__main__":
    main()
