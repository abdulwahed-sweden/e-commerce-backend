"""
Main FastAPI application for Swedish E-commerce Inventory API
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .dependencies import get_db
from .fake_data import create_initial_data

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Swedish E-commerce Inventory API",
    description="A RESTful API for managing inventory for Swedish e-commerce brands",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create initial data on startup
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    create_initial_data(db)
    db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Swedish E-commerce Inventory API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Products endpoints
@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all products with pagination
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product
    """
    return crud.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Warehouses endpoints
@app.get("/warehouses/", response_model=list[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all warehouses with pagination
    """
    warehouses = crud.get_warehouses(db, skip=skip, limit=limit)
    return warehouses

@app.post("/warehouses/", response_model=schemas.Warehouse)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    """
    Create a new warehouse
    """
    return crud.create_warehouse(db=db, warehouse=warehouse)

# Inventory endpoints
@app.get("/inventory/", response_model=list[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all inventory records with pagination
    """
    inventory = crud.get_inventory_items(db, skip=skip, limit=limit)
    return inventory

@app.post("/inventory/", response_model=schemas.Inventory)
def create_inventory_item(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    """
    Create a new inventory record
    """
    return crud.create_inventory_item(db=db, inventory=inventory)

@app.get("/inventory/{product_id}/{warehouse_id}", response_model=schemas.Inventory)
def read_inventory_item(product_id: int, warehouse_id: int, db: Session = Depends(get_db)):
    """
    Get a specific inventory record by product and warehouse IDs
    """
    db_inventory = crud.get_inventory_item(db, product_id=product_id, warehouse_id=warehouse_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

@app.put("/inventory/{product_id}/{warehouse_id}", response_model=schemas.Inventory)
def update_inventory_item(
    product_id: int, 
    warehouse_id: int, 
    inventory_update: schemas.InventoryUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an inventory item's quantity
    """
    return crud.update_inventory_quantity(
        db=db, 
        product_id=product_id, 
        warehouse_id=warehouse_id, 
        quantity=inventory_update.quantity
    )