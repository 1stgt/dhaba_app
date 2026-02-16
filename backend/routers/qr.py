import os
import qrcode
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter(tags=["QR"])

QR_DIR = "static/qr_codes"
if not os.path.exists(QR_DIR):
    os.makedirs(QR_DIR, exist_ok=True)

@router.get("/vendor/qr", response_model=schemas.QRCode)
def get_or_generate_qr(
    current_vendor: models.Vendor = Depends(auth.get_current_vendor),
    db: Session = Depends(database.get_db)
):
    # Check if QR already exists
    db_qr = db.query(models.QRCode).filter(models.QRCode.vendor_id == current_vendor.id).first()
    if db_qr:
        return db_qr

    # Generate Public URL (In production, use actual domain)
    # Using a placeholder for now, frontend should know the base URL
    public_url = f"https://dhabaapp.in/order/{current_vendor.id}"
    
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(public_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save Image
    filename = f"{current_vendor.id}.png"
    file_path = os.path.join(QR_DIR, filename)
    img.save(file_path)

    # Save to DB
    new_qr = models.QRCode(
        vendor_id=current_vendor.id,
        qr_image_path=file_path,
        public_url=public_url
    )
    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)
    return new_qr
