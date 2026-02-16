import sys
import os
# Add current directory to path so we can import backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend import database, models, auth
from sqlalchemy.orm import Session

def seed():
    db = database.SessionLocal()
    
    email = "vendor@dhaba.com"
    password = "password123"
    
    # Check if exists
    existing = db.query(models.Vendor).filter(models.Vendor.email == email).first()
    if existing:
        print(f"Vendor {email} already exists.")
        return

    hashed = auth.get_password_hash(password)
    
    vendor = models.Vendor(
        email=email,
        hashed_password=hashed,
        stall_name="Spicy Dhaba",
        owner_name="Raj Kumar",
        phone_number="9876543210",
        city="Delhi",
        upi_id="raj@upi"
    )
    
    db.add(vendor)
    db.commit()
    print(f"Created vendor: {email} / {password}")
    
    db.close()

if __name__ == "__main__":
    # Ensure tables are created
    models.Base.metadata.create_all(bind=database.engine)
    seed()
