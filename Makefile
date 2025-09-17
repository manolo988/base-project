.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies"
	@echo "  make dev           - Start development environment with Docker"
	@echo "  make build         - Build Docker containers"
	@echo "  make down          - Stop all containers"
	@echo "  make reset         - Reset database and rebuild"
	@echo "  make test          - Run tests"
	@echo "  make migrate       - Run database migrations"
	@echo "  make migration     - Create new migration"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make logs          - Show container logs"
	@echo "  make shell-backend - Access backend container shell"
	@echo "  make shell-db      - Access database shell"

.PHONY: install
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

.PHONY: dev
dev:
	docker-compose up

.PHONY: build
build:
	docker-compose build

.PHONY: down
down:
	docker-compose down

.PHONY: reset
reset:
	docker-compose down -v
	docker-compose up --build

.PHONY: test
test:
	cd backend && pytest app/tests/ -v

.PHONY: test-coverage
test-coverage:
	cd backend && pytest app/tests/ --cov=app --cov-report=html

.PHONY: migrate
migrate:
	cd backend && alembic upgrade head

.PHONY: migration
migration:
	@read -p "Enter migration message: " msg; \
	cd backend && alembic revision --autogenerate -m "$$msg"

.PHONY: lint
lint:
	cd backend && python -m flake8 app/ --max-line-length=100 --exclude=alembic
	cd backend && python -m mypy app/ --ignore-missing-imports
	cd frontend && npm run lint

.PHONY: format
format:
	cd backend && python -m black app/
	cd backend && python -m isort app/
	cd frontend && npm run format

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: shell-backend
shell-backend:
	docker-compose exec backend /bin/bash

.PHONY: shell-db
shell-db:
	docker-compose exec db psql -U postgres -d prototype_db

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf backend/.pytest_cache
	rm -rf backend/htmlcov
	rm -rf frontend/build
	rm -rf frontend/node_modules
	rm -f backend/test.db