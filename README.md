# Full-Stack CRUD Application Boilerplate

A production-ready boilerplate for building full-stack CRUD applications with modern best practices, authentication, and scalable architecture.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with repository pattern
- **PostgreSQL** - Primary database
- **Alembic** - Database migrations
- **JWT Authentication** - Secure token-based auth
- **Pytest** - Testing framework

### Frontend
- **React 18** - UI framework with hooks
- **Context API** - State management
- **Axios** - HTTP client with interceptors
- **JWT Integration** - Token management

### Infrastructure
- **Docker Compose** - Container orchestration
- **Make** - Task automation
- **Pre-commit hooks** - Code quality

## Architecture Features

✅ **Clean Architecture**
- Repository pattern for data access
- Service layer for business logic
- Dependency injection
- Separation of concerns

✅ **Security**
- JWT authentication with refresh tokens
- Password hashing (bcrypt)
- CORS configuration
- Environment-based configuration

✅ **API Best Practices**
- RESTful API design
- API versioning (/api/v1)
- Pagination support
- Comprehensive error handling
- OpenAPI/Swagger documentation

✅ **Testing**
- Unit tests with pytest
- Test fixtures and factories
- Database isolation
- Authentication testing

✅ **Developer Experience**
- Hot reload in development
- Makefile commands
- Pre-commit hooks
- Comprehensive logging

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL (or use Docker)

### Setup

1. **Clone and setup environment:**
```bash
cp .env.example .env
```

2. **Start with Docker (Recommended):**
```bash
make dev
# or
docker-compose up --build
```

3. **Manual Setup (Alternative):**

Backend:
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm start
```

## Available Commands

```bash
make help          # Show all available commands
make dev           # Start development environment
make test          # Run tests
make migrate       # Run database migrations
make lint          # Run code linters
make format        # Format code
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user

### Items (Protected)
- `GET /api/v1/items/` - List items (paginated)
- `POST /api/v1/items/` - Create item
- `GET /api/v1/items/{id}` - Get item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/v1/         # API routes
│   │   ├── core/           # Core configs & security
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── repositories/   # Data access layer
│   │   ├── services/       # Business logic
│   │   └── tests/          # Test suite
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # Context providers
│   │   ├── services/       # API services
│   │   └── App.js
│   └── package.json
├── docker-compose.yml
├── Makefile
└── README.md
```

## Testing

```bash
# Run backend tests
cd backend && pytest

# With coverage
cd backend && pytest --cov=app

# Run specific test
cd backend && pytest app/tests/test_auth.py
```

## Database Migrations

```bash
# Create new migration
make migration

# Apply migrations
make migrate

# Rollback
cd backend && alembic downgrade -1
```

## Default Credentials

For development only:
- Email: `admin@example.com`
- Password: `changeme`

## Environment Variables

Key variables in `.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-secret-key
REACT_APP_API_URL=http://localhost:8000
```

## Production Considerations

Before deploying to production:

1. **Security**
   - Generate strong SECRET_KEY
   - Use environment-specific configs
   - Enable HTTPS/TLS
   - Configure rate limiting
   - Set up monitoring/alerting

2. **Database**
   - Use connection pooling
   - Add indexes for performance
   - Set up backups
   - Use read replicas if needed

3. **API**
   - Add caching (Redis)
   - Implement rate limiting
   - Add request validation
   - Set up CDN for static assets

4. **Monitoring**
   - Application performance monitoring
   - Error tracking (Sentry)
   - Logging aggregation
   - Health checks

## Interview Preparation

This boilerplate demonstrates:

1. **Architecture Skills**
   - Clean code principles
   - Design patterns
   - Scalable structure
   - Separation of concerns

2. **Full-Stack Proficiency**
   - Modern frontend (React)
   - API development (FastAPI)
   - Database design (PostgreSQL)
   - Authentication implementation

3. **Best Practices**
   - Testing strategies
   - Security awareness
   - Documentation
   - DevOps readiness

4. **Ready for Extension**
   - Easy to add new models
   - Modular components
   - Clear patterns to follow
   - Production-ready setup

## License

MIT License - Use freely for your projects and interviews!