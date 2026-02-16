from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter(tags=["Vendor"])

@router.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.email == form_data.username).first()
    if not vendor or not auth.verify_password(form_data.password, vendor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": vendor.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/vendor/me", response_model=schemas.Vendor)
def read_users_me(current_vendor: models.Vendor = Depends(auth.get_current_vendor)):
    return current_vendor

@router.put("/vendor/profile", response_model=schemas.Vendor)
def update_profile(
    vendor_update: schemas.VendorUpdate,
    current_vendor: models.Vendor = Depends(auth.get_current_vendor),
    db: Session = Depends(database.get_db)
):
    # Only update provided fields
    if vendor_update.stall_name: current_vendor.stall_name = vendor_update.stall_name
    if vendor_update.owner_name: current_vendor.owner_name = vendor_update.owner_name
    if vendor_update.phone_number: current_vendor.phone_number = vendor_update.phone_number
    if vendor_update.city: current_vendor.city = vendor_update.city
    if vendor_update.upi_id: current_vendor.upi_id = vendor_update.upi_id
    
    db.commit()
    db.refresh(current_vendor)
    return current_vendor
