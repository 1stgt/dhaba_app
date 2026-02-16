import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import APIClient

st.set_page_config(page_title="QR Code", page_icon="🏁")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")

st.title("🏁 Your QR Code")

if st.button("⬅ Back to Dashboard"):
    st.switch_page("pages/2_Dashboard.py")

qr_data = APIClient.get_qr_code()

if qr_data:
    # Construct image URL (assuming backend is local)
    # The path returned is relative to backend execution, we need to serve it via static mount
    # backend saves to "static/qr_codes/..."
    # backend mounts "/static" -> "static"
    # so url is http://localhost:8000/ + "static/qr_codes/..."
    # But wait, qr_image_path in DB is "static/qr_codes/xxx.png" (from router)
    # Router returns:
    # file_path = os.path.join(QR_DIR, filename) -> "static\qr_codes\xxx.png" on windows?
    # We should normalize path separators or handling in backend.
    
    # Actually, let's just use the logic:
    # If the backend returns "static/qr_codes/uuid.png", then the URL is:
    # http://localhost:8000/static/qr_codes/uuid.png
    
    # We need to extract the filename from the path
    path = qr_data.get("qr_image_path", "")
    filename = os.path.basename(path)
    
    qr_url = f"http://localhost:8000/static/qr_codes/{filename}"
    public_url = qr_data.get("public_url")
    
    st.image(qr_url, caption="Scan to Order", width=300)
    
    st.success(f"Public Ordering URL: {public_url}")
    st.code(public_url)
    
else:
    st.error("Could not fetch QR code. Try updating your profile first.")
