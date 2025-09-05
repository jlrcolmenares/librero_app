# Makefile for Librero App

.PHONY: up clean frontend-test

# Start the application
up:
	@echo "Starting Librero with Docker Compose..."
	@echo "Frontend: http://localhost:80"
	@echo "Backend API: http://localhost/docs"
	docker compose up --build

# Run frontend tests
frontend-test:
	@echo "Running frontend tests..."
	cd frontend && npm install && npm test

# Clean up all resources
clean:
	docker compose down --rmi all --volumes --remove-orphans
	rm -rf .pytest_cache .coverage htmlcov/
