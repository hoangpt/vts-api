# Development Setup

This guide will help you set up the development environment for VTS API.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- PostgreSQL (for production) or SQLite (for development)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/hoangpt/vts-api.git
cd vts-api
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies

#### Windows
```powershell
pip install -r requirements.txt
pip install -r requirements-windows.txt
```

#### Linux/macOS
```bash
# Install system dependencies first
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install -y libmagic1

# RHEL/CentOS:
sudo yum install -y file-libs

# Fedora:
sudo dnf install -y file-libs

# macOS:
brew install libmagic

# Then install Python dependencies
pip install -r requirements.txt
pip install -r requirements-linux.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=sqlite:///./storage/lengkeng.db
IS_PRODUCTION=false

# JWT
JWT_SECRET_KEY=your-secret-key-here

# CORS
ALLOW_CORS_LOCAL=true
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# RabbitMQ (optional)
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=rabbitmq
RABBITMQ_PASSWORD=rabbitmq
```

### 5. Initialize Database

The database will be created automatically on first run. To create an admin user:

```bash
python scripts/create_admin.py
```

Default credentials: `admin` / `admin123`

### 6. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development Scripts

### Windows
```powershell
# Run development server
.\run_dev.ps1
```

### Linux/macOS
```bash
# Make script executable
chmod +x run_dev.sh

# Run development server
./run_dev.sh
```

## Docker Development

### Using Docker Compose

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# Stop containers
docker-compose down
```

### Using Plain Docker

```bash
# Build image
docker build -t vts-api .

# Run container
docker run -d --name vts-api -p 8000:8000 \
  -e ENABLE_CORS=true \
  -v ./storage:/app/storage vts-api
```

## Code Style

Follow the project's code style guidelines:
- Use type hints for function parameters and return values
- Write Google-style docstrings for all public functions
- Keep functions focused and single-purpose
- Use meaningful variable names

## Next Steps

- Read the [Testing Guide](testing.md) to learn about running tests
- Check the [API Reference](../api/overview.md) for API documentation
- Review the [User Service](../api/user-service.md) for example code patterns
