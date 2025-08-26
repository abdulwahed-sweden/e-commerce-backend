"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session

from . import models, schemas

# Product operations
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Warehouse operations
def get_warehouse(db: Session, warehouse_id: int):
    return db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()

def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

# Inventory operations
def get_inventory_item(db: Session, product_id: int, warehouse_id: int):
    return db.query(models.Inventory).filter(
        models.Inventory.product_id == product_id,
        models.Inventory.warehouse_id == warehouse_id
    ).first()

def get_inventory_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()

def create_inventory_item(db: Session, inventory: schemas.InventoryCreate):
    db_inventory = models.Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory_quantity(db: Session, product_id: int, warehouse_id: int, quantity: int):
    db_inventory = get_inventory_item(db, product_id=product_id, warehouse_id=warehouse_id)
    if db_inventory:
        db_inventory.quantity = quantity
        db.commit()
        db.refresh(db_inventory)
    return db_inventory