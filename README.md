# Swedish E-commerce Inventory API

A FastAPI-based RESTful API for managing inventory for Swedish e-commerce brands with JWT authentication and role-based access control.

## 🚀 Features

- **JWT Authentication** - Secure token-based authentication system
- **Role-Based Access Control** - Admin, Manager, and Viewer roles with different permissions
- **Product Management** - Full CRUD operations for products
- **Warehouse Management** - Manage multiple warehouse locations across Sweden
- **Inventory Tracking** - Real-time inventory management across warehouses
- **RESTful API Design** - Clean, well-documented API endpoints
- **PostgreSQL Database** - Robust relational database support
- **Docker Containerization** - Easy deployment with Docker and Docker Compose
- **Automated Testing** - Comprehensive test suite with GitHub Actions CI/CD
- **Swedish Market Focus** - Pre-configured with Swedish products and locations

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **Authentication**: JWT Tokens with bcrypt password hashing
- **ORM**: SQLAlchemy
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus, Grafana, Loki (Ready for integration)
- **CI/CD**: GitHub Actions

## 📋 API Endpoints

### Authentication Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout and invalidate tokens

### Product Endpoints (Requires Authentication)
- `GET /products/` - List all products (All roles)
- `POST /products/` - Create a new product (Admin, Manager)
- `GET /products/{product_id}` - Get product details (All roles)
- `PUT /products/{product_id}` - Update product (Admin, Manager)

### Warehouse Endpoints (Requires Authentication)
- `GET /warehouses/` - List all warehouses (All roles)
- `POST /warehouses/` - Create a new warehouse (Admin, Manager)
- `GET /warehouses/{warehouse_id}` - Get warehouse details (All roles)

### Inventory Endpoints (Requires Authentication)
- `GET /inventory/` - List all inventory items (All roles)
- `POST /inventory/` - Create inventory record (Admin, Manager)
- `GET /inventory/{product_id}/{warehouse_id}` - Get specific inventory item (All roles)
- `PUT /inventory/{product_id}/{warehouse_id}` - Update inventory quantity (Admin, Manager)

### Utility Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## 🔐 User Roles & Permissions

| Role | Permissions | Access Level |
|------|-------------|--------------|
| **Admin** | Full CRUD + User management | Complete system access |
| **Manager** | Read/Write products, warehouses, inventory | Operational management |
| **Viewer** | Read-only access | Monitoring and reporting |

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd swedish-ecommerce-api
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Default Test Users

The system includes these default users with secure passwords:

| Email | Password | Role | Access |
|-------|----------|------|--------|
| `admin@company.se` | `SecureAdmin123` | Admin | Full system access |
| `manager@company.se` | `ManagerPass123` | Manager | Read/Write operations |
| `viewer@company.se` | `ViewerAccess123` | Viewer | Read-only access |

**Note**: All default passwords meet security requirements (8+ characters, uppercase, lowercase, and digit).

## 📁 Project Structure

```
swedish-ecommerce-api/
├── app/
│   ├── api/
│   │   └── endpoints/          # API route handlers
│   ├── core/                   # Core configuration
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   └── utils/                  # Utility functions
├── tests/                      # Test suite
├── migrations/                 # Database migrations
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container configuration
└── requirements.txt            # Python dependencies
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test module
pytest tests/test_auth.py -v
```

## 🔧 Configuration

Environment variables:

```ini
# Database
DATABASE_URL=postgresql://user:password@db:5432/swedish_ecommerce

# JWT Authentication
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
DEBUG=False
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## 📊 Monitoring & Analytics

The API is prepared for integration with:
- **Prometheus** for metrics collection
- **Grafana** for data visualization
- **Loki** for log aggregation

## 🚢 Deployment

### Production Deployment

1. **Set production environment variables**
2. **Build and deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

### Kubernetes Deployment (Optional)

Kubernetes manifests are available in the `k8s/` directory for cluster deployment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🗺️ Roadmap

- [ ] AI-powered demand forecasting integration
- [ ] Real-time inventory notifications
- [ ] Advanced reporting and analytics
- [ ] Multi-language support (Swedish/English)
- [ ] Mobile app companion
- [ ] Third-party API integrations (payment, shipping)

---

**Note**: This is a production-ready API template. Ensure proper security measures are implemented before deploying to production environments.