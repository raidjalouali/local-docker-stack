.PHONY: up down logs test clean

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

test:
	curl -i http://localhost:8080/
	curl -i http://localhost:8080/health
	curl -i http://localhost:8080/db-check

clean:
	docker compose down -v
