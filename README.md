# Veda E-Commerce API

Veda is a robust RESTful API for an e-commerce platform built with Python, Flask, and SQLAlchemy. This API provides complete functionality for user authentication, product management, order processing, and review systems with role-based access control.

## Technologies Used

- **Backend Framework**: Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Werkzeug Security
- **API Development**: Flask-RESTful
- **Database Migrations**: Flask-Migrate
- **Serialization**: SQLAlchemy-Serializer
- **CORS Handling**: Flask-CORS
- **Validation**: SQLAlchemy Validates

## Key Features

1. **User Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control (Admin/Customer)
   - Secure password hashing

2. **Product Management**
   - Public product listings
   - Admin-only product CRUD operations
   - Category-based organization

3. **Order System**
   - User-specific order management
   - Multi-item order support
   - Order status tracking

4. **Review System**
   - Product reviews with ratings
   - User-specific review management
   - Public review listings

5. **Admin Dashboard**
   - User management
   - Category management
   - Order oversight

## Installation Guide

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/veda-ecommerce-api.git
cd veda-ecommerce-api
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
echo "JWT_SECRET_KEY=your_strong_secret_key" > .env
```

5. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Create admin user:
```bash
flask shell
>>> from models import db, User
>>> from werkzeug.security import generate_password_hash
>>> admin = User(username='admin', email='admin@example.com', password=generate_password_hash('adminpassword'), role='admin', phone='1234567890', address='Admin HQ')
>>> db.session.add(admin)
>>> db.session.commit()
```

7. Run the application:
```bash
flask run --port 5555
```

## API Endpoints

### Authentication
| Method | Endpoint    | Description          |
|--------|-------------|----------------------|
| POST   | /register   | Register new user    |
| POST   | /login      | Login and get JWT    |

### Products
| Method | Endpoint            | Access     | Description               |
|--------|---------------------|------------|---------------------------|
| GET    | /products           | Public     | Get all products          |
| GET    | /products/{id}      | Public     | Get single product        |
| POST   | /admin/products     | Admin only | Create new product        |
| PATCH  | /admin/products/{id}| Admin only | Update product            |
| DELETE | /admin/products/{id}| Admin only | Delete product            |

### Orders
| Method | Endpoint          | Access           | Description               |
|--------|-------------------|------------------|---------------------------|
| GET    | /orders           | Authenticated    | Get user's orders         |
| POST   | /orders           | Authenticated    | Create new order          |
| GET    | /orders/{id}      | Owner/Admin      | Get specific order        |
| DELETE | /orders/{id}      | Owner/Admin      | Delete order              |
| POST   | /orders/{id}/items| Owner only       | Add item to order         |

### Categories
| Method | Endpoint       | Access        | Description               |
|--------|----------------|---------------|---------------------------|
| GET    | /categories    | Public        | Get all categories        |
| POST   | /categories    | Admin only    | Create new category       |
| PATCH  | /categories/{id}| Admin only   | Update category           |
| DELETE | /categories/{id}| Admin only   | Delete category           |

### Users
| Method | Endpoint     | Access        | Description               |
|--------|--------------|---------------|---------------------------|
| GET    | /users       | Admin only    | Get all users             |
| GET    | /users/{id}  | Owner/Admin   | Get specific user         |
| PATCH  | /users/{id}  | Owner/Admin   | Update user               |
| DELETE | /users/{id}  | Admin only    | Delete user               |

## Error Handling

The API returns appropriate HTTP status codes:

- 200 OK: Successful GET requests
- 201 Created: Successful resource creation
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing or invalid token
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server-side issues

Error responses include JSON-formatted messages:
```json
{
  "error": "Product not found",
  "code": 404
}
```

## Database Schema

Key tables:
- **users**: Stores user information with roles
- **products**: Product listings with categories
- **orders**: Customer orders with status
- **order_items**: Individual items within orders
- **reviews**: Product reviews with ratings
- **categories**: Product categories

Relationships:
- Users have multiple orders and reviews
- Products belong to categories and have reviews
- Orders contain multiple order items
- Each order item references a product

## Authentication

All endpoints except `/register` and `/login` require authentication. Include JWT in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

JWTs include role claims for authorization:
```json
{
  "identity": 1,
  "role": "admin"
}
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push to your branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact maintainers: Rahma, James, Cheruiyot, Edian and Eugene
