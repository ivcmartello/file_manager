SHELL := /bin/bash

include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(VENV)/bin/activate

.PHONY: install
install: venv ## Make venv and install requirements
	$(BIN)/pip install -r requirements-dev.txt

migrate: ## Make and run migrations
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

.PHONY: super
super: ## Create super user to access admin system
	$(PYTHON) manage.py createsuperuser

.PHONY: test
test: ## Run tests
	DJANGO_SETTINGS_MODULE=file_manager.settings_test coverage erase && coverage run --source="file_manager_app" manage.py test --verbosity=2 --failfast && coverage report -m

.PHONY: run
run: ## Run the Django server
	$(PYTHON) manage.py runserver

start: install migrate run ## Install requirements, apply migrations, then start development server