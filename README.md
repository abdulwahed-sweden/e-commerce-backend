# Swedish E-commerce Inventory API

A FastAPI-based RESTful API for managing inventory for Swedish e-commerce brands.

## Features

- Product management
- Warehouse management
- Inventory tracking
- RESTful API design
- PostgreSQL database
- Docker containerization

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Containerization**: Docker, Docker Compose

## Setup Instructions

1. Clone the repository
2. Install Docker and Docker Compose
3. Run `docker-compose up` to start the application
4. Access the API at `http://localhost:8000`
5. Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /products` - List all products
- `POST /products` - Create a new product
- `GET /warehouses` - List all warehouses
- `POST /warehouses` - Create a new warehouse
- `GET /inventory` - List all inventory items
- `POST /inventory` - Create a new inventory item

## Sample Data

The application includes sample data for:
- Swedish products (Electronics, Fashion, Food, etc.)
- Warehouses in Stockholm, Gothenburg, and Malmö
- Inventory records with random quantities