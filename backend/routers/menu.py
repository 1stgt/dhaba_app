from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, auth

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("/add", response_model=schemas.MenuItem)
def add_menu_item(
    item: schemas.MenuItemCreate,
    current_vendor: models.Vendor = Depends(auth.get_current_vendor),
    db: Session = Depends(database.get_db)
):
    new_item = models.MenuItem(**item.dict(), vendor_id=current_vendor.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/list", response_model=List[schemas.MenuItem])
def list_menu_items(
    current_vendor: models.Vendor = Depends(auth.get_current_vendor),
    db: Session = Depends(database.get_db)
):
    return db.query(models.MenuItem).filter(models.MenuItem.vendor_id == current_vendor.id).all()

@router.put("/update/{item_id}", response_model=schemas.MenuItem)
def update_menu_item(
    item_id: str,
    item_update: schemas.MenuItemUpdate,
    current_vendor: models.Vendor = Depends(auth.get_current_vendor),
    db: Session = Depends(database.get_db)
):
    db_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == item_id,
        models.MenuItem.vendor_id == current_vendor.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item_update.name is not None: db_item.name = item_update.name
    if item_update.description is not None: db_item.description = item_update.description
    if item_update.price is not None: db_item.price = item_update.price
    if item_update.image_url is not None: db_item.image_url = item_update.image_url
    if item_update.is_available is not None: db_item.is_available = item_update.is_available

    db.commit()
    db.refresh(db_item)
    return db_item
