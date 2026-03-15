SHELL := /bin/bash
.ONESHELL:
.PHONY: help init dev-database dev-embedding dev-llm dev-backend dev-frontend dev unit-test-embed-service unit-test-llm-service int-test-llm-service unit-test-backend int-test-backend all-tests stop freeze wait-for-database wait-for-embed-service wait-for-llm-service wait-for-backend-service wait-for-services

help:
	@echo "  make init                       Install all dependencies"
	@echo "  make dev-database               Start Database"
	@echo "  make dev-embedding              Start Embedding Service"
	@echo "  make dev-llm                    Start LLM Service"
	@echo "  make dev-backend                Start Backend"
	@echo "  make dev-frontend               Start Frontend"
	@echo "  make dev                        Start all services"
	@echo "  make unit-test-embed-service    Unit Test Embed Service"
	@echo "  make unit-test-llm-service      Unit Test LLM Service"
	@echo "  make int-test-llm-service       Integration Test LLM Service"
	@echo "  make unit-test-backend          Unit Test Backend"
	@echo "  make int-test-backend           Integration Test Backend"
	@echo "  make all-tests                  Test All Services & Backend"
	@echo "  make stop                       Stop Database, Service, & Backend"
	@echo "  make freeze                     Freeze all dependencies"

# INIT COMMANDS

init:
	cd embedding-service && \
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt && \
	cd ../llm-service && \
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt && \
	cd ../backend && \
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt
	cd frontend && \
	npm install

# USE COMMANDS

dev-database:
	supabase start

dev-embedding:
	cd embedding-service && \
	source venv/bin/activate && \
	uvicorn app.main:app --reload --port 8007

dev-llm:
	cd llm-service && \
	source venv/bin/activate && \
	uvicorn app.main:app --reload --port 8008

dev-backend:
	cd backend && \
	source venv/bin/activate && \
	uvicorn app.main:app --reload --port 8009

dev-frontend:
	cd frontend && \
	npm run dev

dev:
	make dev-database & \
	make dev-backend & \
	make dev-embedding & \
	make dev-llm & \
	make wait-for-services
	sleep 5
	make dev-frontend
	@echo "Everything ready & frontend can be used!"

stop:
	supabase stop --no-backup
	pkill -f "uvicorn app.main:app" || true
	pkill -f "npm run dev" || true

# TESTING COMMANDS

unit-test-embed-service:
	cd embedding-service && \
	source venv/bin/activate && \
	pytest tests

unit-test-llm-service:
	cd llm-service && \
	source venv/bin/activate && \
	pytest tests/unit

int-test-llm-service:
	cd llm-service && \
	source venv/bin/activate && \
	pytest tests/integration -s
	make stop

unit-test-backend:
	make dev-database & \
	make wait-for-database && \
	cd backend && \
	source venv/bin/activate && \
	pytest tests/unit
	make stop

int-test-backend:
	make dev-database & \
	make dev-embedding & \
	make dev-llm & \
	make wait-for-database && \
	make wait-for-embed-service && \
    make wait-for-llm-service && \
	cd backend && \
	source venv/bin/activate && \
	pytest tests/integration
	make stop

all-tests:
	cd embedding-service && \
	source venv/bin/activate && \
	pytest tests && \
	cd .. && \
	cd llm-service && \
	source venv/bin/activate && \
	pytest tests -s && \
	cd ..
	make dev-database & \
	make dev-embedding & \
	make dev-llm & \
	make wait-for-database && \
	make wait-for-embed-service && \
    make wait-for-llm-service && \
	cd backend && \
	source venv/bin/activate && \
	pytest tests -s
	make stop

# UTILITY COMMANDS

freeze:
	cd embedding-service && \
	source venv/bin/activate && \
	pip freeze > requirements.txt && \
	cd ../llm-service && \
	source venv/bin/activate && \
	pip freeze > requirements.txt && \
	cd ../backend && \
	source venv/bin/activate && \
	pip freeze > requirements.txt

wait-for-database:
	@echo "Waiting for database..."
	@timeout 100 bash -c 'until curl -s http://localhost:54321/health > /dev/null 2>&1; do sleep 1; done'
	@echo "Database ready!"

wait-for-embed-service:
	@echo "Waiting for embedding service..."
	@timeout 100 bash -c 'until curl -s http://localhost:8007/health > /dev/null; do sleep 1; done'
	@echo "Embedding service ready!"

wait-for-llm-service:
	@echo "Waiting for LLM service..."
	@timeout 100 bash -c 'until curl -s http://localhost:8008/health > /dev/null; do sleep 1; done'
	@echo "LLM service ready!"

wait-for-backend-service:
	@echo "Waiting for backend service..."
	@timeout 100 bash -c 'until curl -s http://localhost:8009/health > /dev/null; do sleep 1; done'
	@echo "Backend service ready!"

wait-for-services:
	make wait-for-database
	make wait-for-embed-service
	make wait-for-llm-service
	make wait-for-backend-service
	@echo "All services ready!"