from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create-vendor", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(database.get_db)):
    db_vendor = db.query(models.Vendor).filter(models.Vendor.email == vendor.email).first()
    if db_vendor:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(vendor.password)
    new_vendor = models.Vendor(
        email=vendor.email,
        hashed_password=hashed_password,
        stall_name=vendor.stall_name,
        owner_name=vendor.owner_name,
        phone_number=vendor.phone_number,
        city=vendor.city,
        upi_id=vendor.upi_id
    )
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor

@router.get("/vendors", response_model=list[schemas.Vendor])
def list_vendors(db: Session = Depends(database.get_db)):
    return db.query(models.Vendor).all()
