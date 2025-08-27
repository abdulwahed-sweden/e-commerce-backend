"""
Pydantic schemas for request/response validation
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from .models import UserRole

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

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.viewer

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str