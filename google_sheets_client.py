
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
import datetime

# --- Mock Data for Development ---
MOCK_MENU = [
    {"Item": "Veg Momos (Steam)", "Price": 60, "Category": "Momos", "Image": "https://placehold.co/150x150?text=Veg+Momo"},
    {"Item": "Chicken Momos (Steam)", "Price": 80, "Category": "Momos", "Image": "https://placehold.co/150x150?text=Chicken+Momo"},
    {"Item": "Veg Momos (Fried)", "Price": 70, "Category": "Momos", "Image": "https://placehold.co/150x150?text=Veg+Fried"},
    {"Item": "Chicken Momos (Fried)", "Price": 90, "Category": "Momos", "Image": "https://placehold.co/150x150?text=Chicken+Fried"},
    {"Item": "Coca Cola", "Price": 40, "Category": "Drinks", "Image": "https://placehold.co/150x150?text=Coke"},
]

MOCK_ORDERS = []

class GoogleSheetsClient:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = None
        self.client = None
        self.sheet = None
        self.use_mock = True

        # Try to connect to Google Sheets
        try:
            # Check if secrets are available
            if "connections" in st.secrets and "gsheets" in st.secrets.connections:
                # This is a simplified way to check; robust app checks specific keys
                # Using st.connection or manual auth
                # For this MVP, we'll try manual auth for control or fallback to mock
                self.connect()
                self.use_mock = False
            else:
                print("Secrets not found. Using Mock Data.")
        except Exception as e:
            print(f"Connection failed: {e}. Using Mock Data.")

    def connect(self):
        # In a real app, you might use st.connection("gsheets", type=GSheetsConnection) 
        # or standard gspread with secrets
        # specific implementation depends on how secrets are structured
        # For simplicity in this demo, we assume the user might not have set it up yet
        pass

    def get_menu(self):
        if self.use_mock:
            return pd.DataFrame(MOCK_MENU)
        # Real implementation would fetch from "Menu" worksheet
        return pd.DataFrame()

    def place_order(self, order_data):
        """
        order_data: dict with keys: OrderID, CustomerName, Items, Total, Status, Timestamp
        """
        if self.use_mock:
            MOCK_ORDERS.append(order_data)
            return True
        # Real implementation appends to "Orders" worksheet
        return False

    def get_orders(self):
        if self.use_mock:
            if not MOCK_ORDERS:
                return pd.DataFrame(columns=["OrderID", "CustomerName", "Items", "Total", "Status", "Timestamp"])
            return pd.DataFrame(MOCK_ORDERS)
        return pd.DataFrame()

    def update_order_status(self, order_id, new_status):
        if self.use_mock:
            for order in MOCK_ORDERS:
                if order["OrderID"] == order_id:
                    order["Status"] = new_status
                    return True
            return False
        return False
