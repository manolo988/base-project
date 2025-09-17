#!/usr/bin/env python3
"""
Migration Helper Script
Handles database migrations with proper error checking and user guidance
"""

import subprocess
import sys
import os
from pathlib import Path
import importlib.util
import traceback


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_status(message, status="info"):
    """Print colored status messages"""
    if status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
    elif status == "warning":
        print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")
    elif status == "error":
        print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")
    elif status == "info":
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.ENDC}")
    else:
        print(f"   {message}")


def check_database_connection():
    """Check if database is accessible"""
    try:
        result = subprocess.run(
            ["alembic", "current"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print_status("Database connection successful", "success")
            return True
        else:
            print_status("Database connection failed", "error")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_status("Database connection timeout", "error")
        print("   Make sure the database is running:")
        print("   • If using Docker: docker-compose up db")
        print("   • Check DATABASE_URL in .env file")
        return False
    except Exception as e:
        print_status(f"Unexpected error checking database: {e}", "error")
        return False


def get_current_revision():
    """Get current database revision"""
    try:
        result = subprocess.run(
            ["alembic", "current"],
            capture_output=True,
            text=True
        )

        # Parse output to find revision
        for line in result.stdout.split('\n'):
            if line and not line.startswith('INFO'):
                return line.strip()

        # No revision found means database is empty
        return None
    except Exception as e:
        print_status(f"Error getting current revision: {e}", "error")
        return None


def get_latest_revision():
    """Get latest revision from migrations"""
    try:
        result = subprocess.run(
            ["alembic", "heads"],
            capture_output=True,
            text=True
        )

        for line in result.stdout.split('\n'):
            if line and not line.startswith('INFO'):
                # Extract revision ID from output like "abc123 (head)"
                return line.split()[0].strip()

        return None
    except Exception as e:
        print_status(f"Error getting latest revision: {e}", "error")
        return None


def check_pending_migrations():
    """Check if there are pending migrations"""
    current = get_current_revision()
    latest = get_latest_revision()

    if latest is None:
        print_status("No migrations found in alembic/versions/", "warning")
        return False

    if current is None:
        print_status("Database has no migrations applied yet", "warning")
        print(f"   Latest migration available: {latest}")
        return True

    if current != latest and not current.startswith(latest):
        print_status(f"Database is behind on migrations", "warning")
        print(f"   Current: {current}")
        print(f"   Latest:  {latest}")
        return True

    print_status("Database is up to date", "success")
    return False


def validate_models():
    """Check if all models can be imported without errors"""
    models_dir = Path("app/models")
    errors = []

    if not models_dir.exists():
        print_status("Models directory not found", "error")
        return False

    print_status("Validating model files...", "info")

    # Add the backend directory to Python path for imports
    sys.path.insert(0, str(Path.cwd()))

    for model_file in models_dir.glob("*.py"):
        if model_file.name.startswith("__"):
            continue

        try:
            # Try to import the module using __import__
            module_name = f"app.models.{model_file.stem}"
            __import__(module_name)
            print(f"   ✓ {model_file.name}")
        except Exception as e:
            errors.append((model_file.name, str(e)))
            print(f"   ✗ {model_file.name}: {str(e)}")

    if errors:
        print_status(f"Found {len(errors)} model import errors", "error")
        for file, error in errors:
            print(f"\n   {Colors.BOLD}{file}:{Colors.ENDC}")
            # Parse common import errors
            if "ForeignKey" in error:
                print("   → Add: from sqlalchemy import ForeignKey")
            if "BigInteger" in error:
                print("   → Add: from sqlalchemy import BigInteger")
            if "JSONB" in error:
                print("   → Add: from sqlalchemy.dialects.postgresql import JSONB")
            if error not in ["ForeignKey", "BigInteger", "JSONB"]:
                print(f"   → {error}")
        return False

    print_status("All models validated successfully", "success")
    return True


def apply_pending_migrations():
    """Apply pending migrations with user confirmation"""
    response = input(f"\n{Colors.WARNING}Apply pending migrations? (y/n): {Colors.ENDC}")
    if response.lower() == 'y':
        print_status("Applying migrations...", "info")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_status("Migrations applied successfully", "success")
            return True
        else:
            print_status("Failed to apply migrations", "error")
            print(result.stderr)
            return False
    return False


def create_migration(message=None):
    """Create a new migration"""
    if not message:
        message = input(f"\n{Colors.CYAN}Enter migration message: {Colors.ENDC}")

    if not message:
        print_status("Migration message is required", "error")
        return False

    print_status(f"Creating migration: {message}", "info")

    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print_status("Migration created successfully", "success")
        print(result.stdout)

        # Ask if user wants to apply it
        response = input(f"\n{Colors.WARNING}Apply this migration now? (y/n): {Colors.ENDC}")
        if response.lower() == 'y':
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_status("Migration applied successfully", "success")
            else:
                print_status("Failed to apply migration", "error")
                print(result.stderr)

        return True
    else:
        print_status("Failed to create migration", "error")
        print(result.stderr)
        return False


def main():
    """Main migration helper flow"""
    print(f"\n{Colors.BOLD}=== Database Migration Helper ==={Colors.ENDC}\n")

    # Check if running in check-only mode
    check_only = "--check-only" in sys.argv

    # Step 1: Check database connection
    if not check_database_connection():
        print_status("Please fix database connection issues first", "error")
        sys.exit(1)

    # Step 2: Check for pending migrations
    has_pending = check_pending_migrations()

    if check_only:
        # Just report status and exit
        if has_pending:
            print_status("Action required: Apply pending migrations", "warning")
            print(f"   Run: {Colors.BOLD}make migrate{Colors.ENDC}")
        else:
            print_status("Ready to create new migrations", "success")

        # Always validate models in check mode
        validate_models()
        sys.exit(0 if not has_pending else 1)

    # Normal migration creation mode
    if has_pending:
        if apply_pending_migrations():
            # Re-check after applying
            has_pending = check_pending_migrations()
        else:
            print_status("Please apply pending migrations before creating new ones", "warning")
            print(f"   Run: {Colors.BOLD}make migrate{Colors.ENDC}")
            sys.exit(1)

    # Step 3: Validate models
    if not validate_models():
        print_status("Please fix model import errors before creating migration", "error")
        sys.exit(1)

    # Step 4: Create migration if everything is good
    if not has_pending:
        # Get migration message from command line args if provided (excluding --flags)
        args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
        message = " ".join(args) if args else None

        if create_migration(message):
            print_status("Migration process completed successfully!", "success")
        else:
            sys.exit(1)

    print(f"\n{Colors.GREEN}All done!{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Migration helper cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")
        traceback.print_exc()
        sys.exit(1)