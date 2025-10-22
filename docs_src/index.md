# VTS API Documentation

Welcome to the VTS API documentation! This is a comprehensive FastAPI-based system for managing users, templates, file uploads, and AI-generated content for smart report generation.

## Features

- **🔐 JWT Authentication**: Secure login with 8-hour token expiration
- **👑 Role-Based Access Control**: Admin role required for management operations
- **👥 User Management**: Complete CRUD operations for user accounts
- **📋 Template Management**: Create and manage report templates
- **📁 File Upload System**: Handle various file formats for processing
- **🚀 RabbitMQ Integration**: Message queue for file upload notifications
- **🤖 AI Integration**: Generate reports and content using AI
- **🗃️ Multi-Database Support**: PostgreSQL for production, SQLite for development
- **🔍 Search & Filter**: Advanced search functionality across entities
- **✅ Data Validation**: Comprehensive validation and error handling

## Quick Links

- [API Reference](api/overview.md) - Detailed API documentation
- [User Management](api/user-service.md) - User service documentation
- [Development Setup](development/setup.md) - Get started with development
- [Testing Guide](development/testing.md) - Running tests

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/hoangpt/vts-api.git
cd vts-api

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload --port 8000
```

### API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

The project follows a layered architecture:

- **Controllers**: Handle HTTP requests and responses
- **Services**: Contain business logic
- **Repositories**: Handle database operations
- **Models**: Define database schemas
- **DTOs**: Data Transfer Objects for API contracts

## Contributing

Please read our [development guide](development/setup.md) for details on our code style and development process.
