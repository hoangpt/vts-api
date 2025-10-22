# API Overview

The VTS API provides a comprehensive set of endpoints for managing users, templates, and AI-generated content.

## Authentication

All API endpoints (except login) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Base URL

Development: `http://localhost:8000`

## Core Modules

### User Management

The user management module handles all user-related operations including:

- User CRUD operations
- Authentication and authorization
- Role-based access control
- User status management

See [User Service Documentation](user-service.md) for detailed information.

### Configuration

The application uses a flexible configuration system:

- **Database**: Supports both SQLite (development) and PostgreSQL (production)
- **RabbitMQ**: Message queue for asynchronous operations
- **Environment Variables**: Configurable via `.env` file

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "status": "success",
  "data": { ... }
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

Currently, there are no rate limits applied. This may change in production deployments.

## Versioning

The API is currently at version 1.0. Future versions will be indicated in the URL path.
