# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 INTERVIEW CONTEXT

**IMPORTANT**: This is a boilerplate project prepared for technical interviews. When called during an interview:
1. **Check `interview-design.md`** for the specific requirements to implement
2. This boilerplate has been enhanced with production-ready patterns - follow them when adding new features
3. The architecture is designed for quick extension - use existing patterns for consistency
4. All authentication, error handling, and basic CRUD operations are already implemented

## Project Overview

This is a **production-ready** full-stack application boilerplate with:
- **Backend**: Python FastAPI with clean architecture (repository pattern, service layer, JWT auth)
- **Frontend**: React 18 with Context API, authentication flow, and modern UI
- **Infrastructure**: Docker containerization, Alembic migrations, testing setup

### Key Features Already Implemented
- ✅ JWT Authentication (login, register, protected routes)
- ✅ Clean Architecture (repositories, services, dependency injection)
- ✅ API Versioning (/api/v1)
- ✅ Database Migrations (Alembic)
- ✅ Comprehensive Testing (pytest)
- ✅ Error Handling & Logging
- ✅ Pagination Support
- ✅ CORS Configuration
- ✅ User Management
- ✅ Item CRUD with ownership

## Development Commands

### Quick Start
```bash
# Start all services (recommended for development)
docker-compose up --build

# Or use Makefile
make dev

# Run tests
make test

# Create new migration
make migration

# Apply migrations
make migrate
```

### Individual Service Commands

#### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development
```bash
cd frontend
npm install
npm start
```

## Project Architecture

### Backend Structure (`backend/app/`)
```
app/
├── api/v1/
│   ├── endpoints/      # Route handlers
│   │   ├── auth.py     # Login, register endpoints
│   │   ├── items.py    # Item CRUD endpoints
│   │   └── users.py    # User management endpoints
│   └── api.py          # Router aggregation
├── core/
│   ├── config.py       # Settings & configuration
│   ├── security.py     # JWT & password hashing
│   ├── dependencies.py # FastAPI dependencies
│   ├── exceptions.py   # Custom exceptions
│   └── logging.py      # Logging configuration
├── models/             # SQLAlchemy models
│   ├── user.py        # User model with relationships
│   └── item.py        # Item model with ownership
├── schemas/            # Pydantic schemas
│   ├── user.py        # User schemas
│   ├── item.py        # Item schemas
│   ├── auth.py        # Auth schemas
│   └── common.py      # Shared schemas (pagination)
├── repositories/       # Data access layer
│   ├── base.py        # Base repository class
│   ├── user.py        # User repository
│   └── item.py        # Item repository
├── services/           # Business logic layer
└── tests/             # Test suite
    ├── conftest.py    # Test fixtures
    ├── test_auth.py   # Auth tests
    └── test_items.py  # Item tests
```

### Frontend Structure (`frontend/src/`)
```
src/
├── components/
│   ├── ItemForm.js    # Item create/edit form
│   ├── ItemList.js    # Items display
│   ├── Login.js       # Login form
│   └── Register.js    # Registration form
├── contexts/
│   └── AuthContext.js # Authentication state
├── services/
│   └── api.js         # API client with interceptors
└── App.js             # Main app with routing logic
```

## API Endpoints

### Authentication (`/api/v1/auth/`)
- `POST /login` - User login (returns JWT token)
- `POST /register` - User registration

### Users (`/api/v1/users/`)
- `GET /me` - Get current user
- `PUT /me` - Update current user
- `GET /` - List all users (admin only)
- `GET /{id}` - Get user by ID (admin only)

### Items (`/api/v1/items/`)
- `GET /` - List user's items (paginated)
- `POST /` - Create new item
- `GET /{id}` - Get item by ID
- `PUT /{id}` - Update item
- `DELETE /{id}` - Delete item

## Adding New Features (Interview Pattern Guide)

### 1. Adding a New Model
```python
# 1. Create model in app/models/your_model.py
# 2. Create schemas in app/schemas/your_model.py
# 3. Create repository in app/repositories/your_model.py (extend BaseRepository)
# 4. Create endpoints in app/api/v1/endpoints/your_endpoint.py
# 5. Add router to app/api/v1/api.py
# 6. Create migration: make migration
```

### 2. Adding New Endpoints
Follow the pattern in `app/api/v1/endpoints/items.py`:
- Use dependency injection for database and auth
- Return proper HTTP status codes
- Use Pydantic schemas for validation
- Include pagination where applicable

### 3. Adding Frontend Components
Follow the pattern in existing components:
- Use AuthContext for user state
- Handle loading and error states
- Use the api service for all API calls

## Database Schema

### User Model
- `id`: Primary key
- `email`: Unique email
- `hashed_password`: Bcrypt hashed
- `full_name`: Optional
- `is_active`: Boolean
- `is_superuser`: Boolean
- `created_at`, `updated_at`: Timestamps

### Item Model
- `id`: Primary key
- `title`: Required string
- `description`: Optional text
- `price`: Float (default 0.0)
- `is_active`: Boolean
- `owner_id`: Foreign key to User
- `created_at`, `updated_at`: Timestamps

## Key URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Database: localhost:5432

## Environment Variables
Key variables in `.env`:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `REACT_APP_API_URL`: Backend URL for frontend

## Important Notes for Interview

1. **Authentication is already handled** - Use the existing JWT system
2. **Follow the repository pattern** - Extend BaseRepository for new models
3. **Use existing error handling** - Custom exceptions are in core/exceptions.py
4. **Pagination is built-in** - See PaginatedResponse schema
5. **Testing infrastructure ready** - Add tests following existing patterns
6. **Database migrations ready** - Use Alembic for schema changes
7. **CORS is configured** - No need to modify for localhost development

## When Implementing Interview Requirements

1. **First check `interview-design.md`** for specific requirements
2. **Follow existing patterns** - The codebase demonstrates best practices
3. **Use the repository pattern** for data access
4. **Add proper tests** for new features
5. **Create migrations** for database changes
6. **Update API documentation** (happens automatically with FastAPI)

Remember: This boilerplate is designed to let you focus on implementing business logic rather than infrastructure setup!