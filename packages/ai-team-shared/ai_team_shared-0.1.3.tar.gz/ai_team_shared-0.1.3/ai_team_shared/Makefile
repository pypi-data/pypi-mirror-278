# Makefile for Alembic database migrations and SQL data model development

# Variables
ALEMBIC_CONFIG = alembic.ini
MIGRATION_SCRIPT = scripts/db_migration.py

# Default target
all: help

# Show help message
help:
	@echo "Available commands:"
	@echo "  make migrate_up    Run database migration to the latest revision (head)"
	@echo "  make migrate_down  Rollback database migration to the previous revision (head-1)"
	@echo "  make generate_migration  Generate a new migration script based on changes in models"
	@echo "  make autogenerate_migration  Autogenerate a migration script based on changes in models"
	@echo "  make revision_history  Show the revision history of the database"
	@echo "  make current_revision  Show the current revision of the database"

# Run database migration to the latest revision (head)
migrate_up:
	python $(MIGRATION_SCRIPT) up

# Rollback database migration to the previous revision (head-1)
migrate_down:
	python $(MIGRATION_SCRIPT) down

# Generate a new migration script based on changes in models
generate_migration:
	alembic -c $(ALEMBIC_CONFIG) revision --autogenerate -m "migration-$(shell date +'%Y%m%d%H%M%S')"

# Show the revision history of the database
revision_history:
	alembic -c $(ALEMBIC_CONFIG) history

# Show the current revision of the database
current_revision:
	alembic -c $(ALEMBIC_CONFIG) current

# Run tests for SQL data models if any
test_models:
	pytest tests/models/

# Support these for running on CLI
## Format SQL data model files using black
#format_models:
#	black models/
#
## Lint SQL data model files using flake8
#lint_models:
#	flake8 models/
#
## Check type annotations in SQL data model files using mypy
#typecheck_models:
#	mypy models/

publish:
	poetry build
	poetry publish

.PHONY: all help migrate_up migrate_down generate_migration autogenerate_migration revision_history current_revision test_models
