from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Vendor Schemas ---
class VendorBase(BaseModel):
    stall_name: str
    owner_name: str
    phone_number: str
    city: str
    email: str
    upi_id: Optional[str] = None

class VendorCreate(VendorBase):
    password: str

class VendorUpdate(BaseModel):
    stall_name: Optional[str] = None
    owner_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    upi_id: Optional[str] = None

class Vendor(VendorBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Menu Schemas ---
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    image_url: Optional[str] = None
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

class MenuItem(MenuItemBase):
    id: str
    vendor_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- QR Schemas ---
class QRCode(BaseModel):
    id: str
    vendor_id: str
    qr_image_path: str
    public_url: str
    created_at: datetime

    class Config:
        from_attributes = True
