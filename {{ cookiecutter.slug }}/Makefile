SHELL := /bin/bash
.DEFAULT_GOAL := help

# Variables
CURRENT_DIR := $(shell pwd)
COMPOSE_PROJECT := {{ cookiecutter.slug }}
DEV_COMPOSE_FILE := docker-compose.dev.yml
DEV_COMPOSE_COMMAND := docker compose -f $(DEV_COMPOSE_FILE) -p $(COMPOSE_PROJECT)
COMPOSE_FILE := docker-compose.yml
COMPOSE_COMMAND := docker compose -f $(COMPOSE_FILE) -p $(COMPOSE_PROJECT)
SRC_DIRS = ./backend
BLACK_OPTS = ${SRC_DIRS} --exclude migrations

###### Development

up.dev: ## Start the development environment
	$(DEV_COMPOSE_COMMAND) up --remove-orphans

down.dev: ## Stop the development environment
	$(DEV_COMPOSE_COMMAND) down --remove-orphans

build.dev: ## Build the development images
	$(DEV_COMPOSE_COMMAND) build

superuser.dev: ## Creates a Suepruser for your django app in development
	$(DEV_COMPOSE_COMMAND) exec -it api ./manage.py createsuperuser

doc: ## Starts development server for documentation
	mkdocs serve

doc-build: ## Build HTML documentation
	mkdocs build

logs.dev: ## View logs for a specific service in development (usage: make logs.dev <service_name>)
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Please specify a service name. Usage: make logs.dev <service_name>"; \
	else \
		$(DEV_COMPOSE_COMMAND) logs -f $(filter-out $@,$(MAKECMDGOALS)); \
	fi

exec.dev: ## Execute a command in a running container in development (usage: make exec.dev <service_name> <command>)
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo "Please specify a service name and command. Usage: make exec.dev <service_name> <command>"; \
	else \
		$(DEV_COMPOSE_COMMAND) exec $(word 2,$(MAKECMDGOALS)) $(wordlist 3,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)); \
	fi

###### Production

up.prod: ## Start the production environment
	$(COMPOSE_COMMAND) up --remove-orphans

build.prod: ## Build the production images
	$(COMPOSE_COMMAND) build

superuser.prod: ## Creates a Suepruser for your django app in production
	$(COMPOSE_COMMAND) exec -it api ./manage.py createsuperuser

logs.prod: ## View logs for a specific service in production (usage: make logs.prod <service_name>)
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Please specify a service name. Usage: make logs.prod <service_name>"; \
	else \
		$(COMPOSE_COMMAND) logs -f $(filter-out $@,$(MAKECMDGOALS)); \
	fi

exec.prod: ## Execute a command in a running container in production (usage: make exec.prod <service_name> <command>)
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo "Please specify a service name and command. Usage: make exec.prod <service_name> <command>"; \
	else \
		$(COMPOSE_COMMAND) exec $(word 2,$(MAKECMDGOALS)) $(wordlist 3,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)); \
	fi

###### Additional commands

clean: ## Clean up pycache files
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} +

compile-requirements: ## Compile requirements files
	pip-compile backend/requirements/base.in
	pip-compile backend/requirements/dev.in
	pip-compile backend/requirements/docs.in
	pip-compile backend/requirements/production.in

upgrade-requirements: ## Upgrade requirements files
	pip-compile --upgrade backend/requirements/base.in
	pip-compile --upgrade backend/requirements/dev.in
	pip-compile --upgrade backend/requirements/docs.in
	pip-compile --upgrade backend/requirements/production.in

requirements.dev:  ## Install development requrements
	pip install -qr backend/requirements/dev.txt
	pip install -qr backend/requirements/docs.txt

requirements.prod:  ## Install production requrements
	pip install -qr backend/requirements/production.txt

format: ## Format code automatically
	isort ${SRC_DIRS}
	black $(BLACK_OPTS)

test-format: ## Run code formatting tests
	black --check --diff $(BLACK_OPTS)

test-lint: ## Run code linting tests
	flake8 backend

pytest:
	pytest backend

test: test-format test-lint pytest ## Run tests


ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_.-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

# This allows for passing arguments to make targets
%:
	@:
