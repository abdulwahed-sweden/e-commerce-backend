"""
Pydantic schemas for request/response validation
"""
from typing import Optional
from pydantic import BaseModel

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    brand: Optional[str] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # Replaces orm_mode = True in Pydantic v2

# Warehouse schemas
class WarehouseBase(BaseModel):
    name: str
    city: str
    address: Optional[str] = None
    postcode: Optional[str] = None
    capacity: Optional[int] = None

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int

    class Config:
        from_attributes = True

# Inventory schemas
class InventoryBase(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int
    minimum_stock_level: Optional[int] = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int

class Inventory(InventoryBase):
    id: int

    class Config:
        from_attributes = True