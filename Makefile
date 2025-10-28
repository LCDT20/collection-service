.PHONY: help install build up down restart logs test clean migrate shell db-shell

help:
	@echo "Collection Service - TakeYourTrade"
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  make install      - Installa dipendenze Python"
	@echo "  make build        - Builda immagini Docker"
	@echo "  make up           - Avvia servizi Docker"
	@echo "  make down         - Ferma servizi Docker"
	@echo "  make restart      - Riavvia servizi"
	@echo "  make logs         - Mostra logs"
	@echo "  make test         - Esegui test"
	@echo "  make clean        - Pulisci cache e dati"
	@echo "  make migrate      - Esegui migrazioni database"
	@echo "  make shell        - Apri shell nel container app"
	@echo "  make db-shell     - Apri shell MySQL"
	@echo "  make dev          - Avvia in modalità sviluppo"
	@echo "  make run          - Avvia uvicorn locale"

install:
	pip install -r requirements.txt

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f app

test:
	pytest -v

test-watch:
	pytest-watch

test-cov:
	pytest --cov=app --cov-report=html

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf htmlcov

migrate:
	docker exec -it collection_service alembic upgrade head

migrate-create:
	docker exec -it collection_service alembic revision --autogenerate -m "$(msg)"

migrate-downgrade:
	docker exec -it collection_service alembic downgrade -1

shell:
	docker exec -it collection_service /bin/bash

db-shell:
	docker exec -it collection_db mysql -u collection_user -pcollection_password collection_db

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

lint:
	flake8 app tests
	black app tests --check
	isort app tests --check-only

format:
	black app tests
	isort app tests

