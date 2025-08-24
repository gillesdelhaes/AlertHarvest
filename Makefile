# Makefile for AlertHarvest
# Usage: make <target> ENV=dev|prod
# Default: dev

PROJECT_NAME=alertharvest
ENV ?= dev
COMPOSE=docker compose -f docker-compose.$(ENV).yml

# Default target
.DEFAULT_GOAL := help

.PHONY: up down restart logs ps build rebuild shell-django shell-worker migrate makemigrations collectstatic flush health help


# Containers
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart: down up

build:
	$(COMPOSE) build --no-cache

# Full rebuild + start
rebuild: down build up

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

shell-django:
	$(COMPOSE) exec django bash

shell-worker:
	$(COMPOSE) exec worker bash

# Django management commands
migrate:
	$(COMPOSE) exec django python manage.py migrate

makemigrations:
	$(COMPOSE) exec django python manage.py makemigrations

collectstatic:
	$(COMPOSE) exec django python manage.py collectstatic --noinput

# Database cleanup (use with care!)
flush:
	$(COMPOSE) exec django python manage.py flush --noinput

# Healthcheck
health:
	@if [ "$(ENV)" = "prod" ]; then \
		curl -f http://localhost/health/ || (echo "Health check failed" && exit 1); \
	else \
		curl -f http://localhost:8000/health/ || (echo "Health check failed" && exit 1); \
	fi

# Show available targets
help:
	@echo "Usage: make <target> [ENV=dev|prod]"
	@echo ""
	@echo "Targets:"
	@echo "  up                  Start services"
	@echo "  down                Stop services"
	@echo "  restart             Restart services"
	@echo "  build               Build images"
	@echo "  rebuild             Full rebuild and restart"
	@echo "  logs                Tail logs"
	@echo "  ps                  Show running containers"
	@echo "  shell-django        Open Django shell"
	@echo "  shell-worker        Open Worker shell"
	@echo "  migrate             Apply DB migrations"
	@echo "  makemigrations      Create DB migrations"
	@echo "  collectstatic       Collect static files"
	@echo "  flush               Database cleanup (use with care!)"
	@echo "  health              Run health check (port 8000 dev / 80 prod)"
	@echo "  help                Show this help"