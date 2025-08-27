"""
Main FastAPI application for Swedish E-commerce Inventory API
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .dependencies import get_db, require_admin, require_admin_or_manager, require_any_role
from .fake_data import create_initial_data
from .auth_routes import router as auth_router

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

# Include authentication routes
app.include_router(auth_router)

# Add dependency for the /me endpoint
from .dependencies import get_current_active_user

@auth_router.get("/me", response_model=schemas.User)
def get_current_user_info_fixed(
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get current user information
    """
    return current_user

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
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_any_role)
):
    """
    Retrieve all products with pagination (requires authentication)
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_or_manager)
):
    """
    Create a new product (admin/manager only)
    """
    return crud.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_any_role)
):
    """
    Get a specific product by ID (requires authentication)
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Warehouses endpoints
@app.get("/warehouses/", response_model=list[schemas.Warehouse])
def read_warehouses(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_any_role)
):
    """
    Retrieve all warehouses with pagination (requires authentication)
    """
    warehouses = crud.get_warehouses(db, skip=skip, limit=limit)
    return warehouses

@app.post("/warehouses/", response_model=schemas.Warehouse)
def create_warehouse(
    warehouse: schemas.WarehouseCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_or_manager)
):
    """
    Create a new warehouse (admin/manager only)
    """
    return crud.create_warehouse(db=db, warehouse=warehouse)

# Inventory endpoints
@app.get("/inventory/", response_model=list[schemas.Inventory])
def read_inventory(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_any_role)
):
    """
    Retrieve all inventory records with pagination (requires authentication)
    """
    inventory = crud.get_inventory_items(db, skip=skip, limit=limit)
    return inventory

@app.post("/inventory/", response_model=schemas.Inventory)
def create_inventory_item(
    inventory: schemas.InventoryCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_or_manager)
):
    """
    Create a new inventory record (admin/manager only)
    """
    return crud.create_inventory_item(db=db, inventory=inventory)

@app.get("/inventory/{product_id}/{warehouse_id}", response_model=schemas.Inventory)
def read_inventory_item(
    product_id: int, 
    warehouse_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_any_role)
):
    """
    Get a specific inventory record by product and warehouse IDs (requires authentication)
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
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_or_manager)
):
    """
    Update an inventory item's quantity (admin/manager only)
    """
    return crud.update_inventory_quantity(
        db=db, 
        product_id=product_id, 
        warehouse_id=warehouse_id, 
        quantity=inventory_update.quantity
    )

# Admin-only user management endpoints
@app.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    """
    Retrieve all users (admin only)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    """
    Get a specific user by ID (admin only)
    """
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user