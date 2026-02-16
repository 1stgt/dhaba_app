import requests
import streamlit as st

API_URL = "http://localhost:8000"

class APIClient:
    @staticmethod
    def login(email, password):
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                data={"username": email, "password": password}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return {"error": "Invalid credentials"}
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_header():
        token = st.session_state.get("token")
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    @staticmethod
    def get_vendor_profile():
        try:
            response = requests.get(f"{API_URL}/vendor/me", headers=APIClient.get_header())
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def update_profile(data):
        try:
            response = requests.put(f"{API_URL}/vendor/profile", json=data, headers=APIClient.get_header())
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_menu_items():
        try:
            response = requests.get(f"{API_URL}/menu/list", headers=APIClient.get_header())
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    @staticmethod
    def add_menu_item(data):
        try:
            response = requests.post(f"{API_URL}/menu/add", json=data, headers=APIClient.get_header())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_menu_item(item_id, data):
        try:
            response = requests.put(f"{API_URL}/menu/update/{item_id}", json=data, headers=APIClient.get_header())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_qr_code():
        try:
            response = requests.get(f"{API_URL}/vendor/qr", headers=APIClient.get_header())
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
