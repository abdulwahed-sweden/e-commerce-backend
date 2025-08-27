"""
Generate initial fake data for Swedish e-commerce
"""
from sqlalchemy.orm import Session

from . import models, crud
from .auth_utils import get_password_hash

def create_initial_data(db: Session):
    """
    Create initial fake data for the database
    """
    # Check if data already exists
    if db.query(models.Product).count() > 0:
        return  # Data already exists
    
    # Create initial users
    users_data = [
        {
            "email": "admin@company.se",
            "hashed_password": get_password_hash("admin123"),
            "role": models.UserRole.admin,
            "is_active": True
        },
        {
            "email": "manager@company.se", 
            "hashed_password": get_password_hash("manager123"),
            "role": models.UserRole.manager,
            "is_active": True
        },
        {
            "email": "viewer@company.se",
            "hashed_password": get_password_hash("viewer123"),
            "role": models.UserRole.viewer,
            "is_active": True
        }
    ]
    
    # Create users
    for user_data in users_data:
        user = models.User(**user_data)
        db.add(user)
    
    db.commit()

    # Create products (common Swedish e-commerce items)
    products_data = [
        {
            "name": "iPhone 15 Pro", 
            "description": "Latest Apple smartphone with advanced camera system", 
            "price": 12990.0, 
            "category": "Electronics",
            "brand": "Apple"
        },
        {
            "name": "Samsung OLED TV", 
            "description": "55 inch 4K Smart TV with Quantum Processor", 
            "price": 7990.0, 
            "category": "Electronics",
            "brand": "Samsung"
        },
        {
            "name": "Fjällräven Kånken Backpack", 
            "description": "Iconic Swedish backpack made from durable Vinylon F material", 
            "price": 895.0, 
            "category": "Fashion",
            "brand": "Fjällräven"
        },
        {
            "name": "Semper Gluten-Free Pasta", 
            "description": "Organic gluten-free pasta made in Sweden", 
            "price": 29.95, 
            "category": "Food",
            "brand": "Semper"
        },
        {
            "name": "IKEA POÄNG Armchair", 
            "description": "Comfortable reading chair with curved frame", 
            "price": 1495.0, 
            "category": "Furniture",
            "brand": "IKEA"
        },
        {
            "name": "H&M Cotton T-Shirt", 
            "description": "Basic crewneck t-shirt made from organic cotton", 
            "price": 99.0, 
            "category": "Fashion",
            "brand": "H&M"
        },
        {
            "name": "Arla Köttfärs", 
            "description": "Minced meat 500g from Swedish farms", 
            "price": 59.90, 
            "category": "Food",
            "brand": "Arla"
        },
        {
            "name": "Spotify Gift Card", 
            "description": "100 SEK digital gift card for Spotify Premium", 
            "price": 100.0, 
            "category": "Gift Cards",
            "brand": "Spotify"
        },
        {
            "name": "Volvo Car Model", 
            "description": "Die-cast model of a Volvo XC90", 
            "price": 299.0, 
            "category": "Toys",
            "brand": "Volvo"
        },
        {
            "name": "Systembolaget Wine Glass", 
            "description": "Set of 6 premium wine glasses", 
            "price": 249.0, 
            "category": "Home",
            "brand": "Systembolaget"
        },
    ]

    # Create warehouses in Swedish cities
    warehouses_data = [
        {
            "name": "Main Stockholm Warehouse", 
            "city": "Stockholm", 
            "address": "Hammarby Fabriksväg 23", 
            "postcode": "12030",
            "capacity": 5000
        },
        {
            "name": "Gothenburg Distribution Center", 
            "city": "Gothenburg", 
            "address": "Ringön 15", 
            "postcode": "41707",
            "capacity": 3500
        },
        {
            "name": "Malmö Logistics Hub", 
            "city": "Malmö", 
            "address": "Sundstorget 7", 
            "postcode": "21120",
            "capacity": 2800
        },
    ]

    # Create products and warehouses
    products = []
    for product_data in products_data:
        product = models.Product(**product_data)
        db.add(product)
        products.append(product)
    
    warehouses = []
    for warehouse_data in warehouses_data:
        warehouse = models.Warehouse(**warehouse_data)
        db.add(warehouse)
        warehouses.append(warehouse)
    
    db.commit()
    
    # Create inventory items
    import random
    for product in products:
        for warehouse in warehouses:
            inventory_data = {
                "product_id": product.id,
                "warehouse_id": warehouse.id,
                "quantity": random.randint(0, 200),
                "minimum_stock_level": 10
            }
            inventory = models.Inventory(**inventory_data)
            db.add(inventory)
    
    db.commit()