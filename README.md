# Auto-Document

An automated assistant that converts RPA processes into clear, standardized technical documentation

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- RESTful API built with FastAPI
- React-based frontend with Vite
- MySQL database with SQLAlchemy ORM
- Docker support for easy deployment
- CORS-enabled backend
- Password hashing

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **MySQL** - Relational database
- **PyMySQL** - MySQL driver
- **Passlib & Bcrypt** - Password hashing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Git** - Version control

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** and npm - [Download Node.js](https://nodejs.org/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/) (or use Docker)
- **Docker & Docker Compose** (optional) - [Download Docker](https://www.docker.com/products/docker-desktop)
- **Git** - [Download Git](https://git-scm.com/downloads)

## Project Structure

```
Auto-Document/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── security.py       # Password hashing utilities
│   │   ├── models/
│   │   │   └── user.py           # User database model
│   │   ├── routers/
│   │   │   └── auth.py           # Authentication endpoints
│   │   ├── schemas/
│   │   │   └── user.py           # Pydantic schemas
│   │   ├── database.py           # Database configuration
│   │   └── main.py               # FastAPI application entry
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                      # Environment variables (create this)
├── frontend/
│   ├── src/
│   ├── eslint.config.mjs
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Auto-Document
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

## Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Database Configuration
DB_USER=autodoc_user
DB_PASSWORD=autodoc_pass
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=autodoc

# Alternative: Use full DATABASE_URL
# DATABASE_URL=mysql+pymysql://autodoc_user:autodoc_pass@127.0.0.1:3306/autodoc

# Note: When using Docker, set DB_HOST=db
```

### Important Notes:
- For **local development**: Set `DB_HOST=127.0.0.1`
- For **Docker deployment**: Set `DB_HOST=db`
- Never commit `.env` files to version control (already in `.gitignore`)

## Running the Project

### Option 1: Local Development (Recommended for Development)

#### Step 1: Start MySQL Database

**Using Docker Compose:**
```bash
# From project root
docker-compose up -d
```

This starts only the MySQL database on port 3306.

**Or using local MySQL:**
- Ensure MySQL is running locally
- Create database: `CREATE DATABASE autodoc;`
- Create user and grant permissions

#### Step 2: Start Backend

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### Step 3: Start Frontend

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173` (or `http://localhost:5174`)

### Option 2: Full Docker Deployment

```bash
# Uncomment the backend service in docker-compose.yml first

# Start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

To stop services:
```bash
docker-compose down
```

## API Documentation

Once the backend is running, access the automatically generated API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

#### Authentication

**POST** `/auth/register`
- Register a new user
- Request body:
  ```json
  {
    "username": "string",
    "email": "string",
    "full_name": "string",
    "password": "string"
  }
  ```

**POST** `/auth/login`
- Login with existing credentials
- Request body:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

**GET** `/`
- Health check endpoint
- Returns: `{"status": "ok"}`

## 🔧 Development

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Code Linting

```bash
# Backend linting (recommended: install ruff or flake8)
cd backend
ruff check .

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

The application currently uses SQLAlchemy with automatic table creation. For production, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
# Configure alembic.ini and create migrations
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Use ESLint configuration for JavaScript/React code
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Database connection errors:**
- Verify MySQL is running: `docker-compose ps` or `mysql -u root -p`
- Check `.env` file has correct credentials
- Ensure `DB_HOST` is set correctly (127.0.0.1 for local, db for Docker)

**Port already in use:**
- Backend (8000): Check if another process is using the port
- Frontend (5173/5174): Vite will automatically try the next available port
- MySQL (3306): Stop other MySQL instances or change the port in `docker-compose.yml`

**Module not found errors:**
- Backend: Ensure virtual environment is activated and dependencies are installed
- Frontend: Run `npm install` to install all dependencies

**CORS errors:**
- Verify frontend URL is listed in `allow_origins` in `backend/app/main.py`
- Check that both servers are running
