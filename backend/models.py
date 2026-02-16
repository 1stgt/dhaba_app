import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .database import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stall_name = Column(String, index=True)
    owner_name = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    upi_id = Column(String, nullable=True)
    city = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("MenuItem", back_populates="vendor")
    qr_code = relationship("QRCode", back_populates="vendor", uselist=False)


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_id = Column(String, ForeignKey("vendors.id"))
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)  # Storing price in smallest unit (e.g., paisa) or just integer rupees
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vendor = relationship("Vendor", back_populates="items")


class QRCode(Base):
    __tablename__ = "qr_codes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_id = Column(String, ForeignKey("vendors.id"), unique=True)
    qr_image_path = Column(String)
    public_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    vendor = relationship("Vendor", back_populates="qr_code")
