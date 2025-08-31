# Makefile for Librero App

.PHONY: up clean

# Start the application
up:
	@echo "Starting Librero with Docker Compose..."
	@echo "Frontend: http://localhost:80"
	@echo "Backend API: http://localhost/docs"
	docker compose up --build

# Clean up all resources
clean:
	docker compose down --rmi all --volumes --remove-orphans
	rm -rf .pytest_cache .coverage htmlcov/
