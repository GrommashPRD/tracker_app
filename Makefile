APP_NAME = tracker

DB_CONTAINER_NAME = tracker_db

start:
	@docker build -t $(APP_NAME) .
	@docker-compose up -d

stop:
	@docker-compose down

test:
	@docker-compose down
	@docker stop $(DB_CONTAINER_NAME) || exit 0
	@docker pull postgres:17
	@docker run --rm --name $(DB_CONTAINER_NAME) \
	    -e POSTGRES_PASSWORD=postgres \
	    -e POSTGRES_USER=postgres \
	    -e POSTGRES_DB=postgres \
	    -d -p 5432:5432 postgres:17
	@container_name=$(DB_CONTAINER_NAME); \
    pattern="ready to accept connections"; \
    while ! docker logs "$$container_name" | grep -q "$$pattern"; do \
      echo "Waiting for the container to be ready..."; \
      sleep 0.1; \
    done; \
    echo "Container is ready"
	@python manage.py migrate
	@pytest
	@docker stop $(DB_CONTAINER_NAME)

migrate:
	@docker-compose run web python manage.py migrate

.PHONY: start stop test migrate makemigrations

