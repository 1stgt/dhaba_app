from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, vendor, menu, qr
from .database import engine, Base

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dhaba App Vendor Onboarding MVP")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (for QR codes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
app.include_router(admin.router)
app.include_router(vendor.router)
app.include_router(menu.router)
app.include_router(qr.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Dhaba App Vendor API"}
