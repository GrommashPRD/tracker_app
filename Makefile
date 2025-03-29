VENV_DIR = venv
REQUIREMENTS = req.txt

start:
	@docker build -t tracker .
	@docker-compose up -d

stop:
	@docker-compose down

test:
	@docker-compose down
	@docker stop test_postgres || exit 0
	@docker pull postgres:17
	@docker run --rm --name test_postgres \
	    -e POSTGRES_PASSWORD=postgres \
	    -e POSTGRES_USER=postgres \
	    -e POSTGRES_DB=tracker \
	    -d -p 54321:5432 postgres:17
	@container_name=test_postgres; \
	pattern="ready to accept connections"; \
	while ! docker logs "$$container_name" | grep -q "$$pattern"; do \
	  echo "Waiting for the container to be ready..."; \
	  sleep 0.1; \
	done; \
	echo "Container is ready"
	@python manage.py migrate
	@python -m pytest
	@docker stop test_postgres

migrate:
	@docker-compose run web python manage.py migrate

venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi

install: venv
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

clean:
	@rm -rf $(VENV_DIR)

.PHONY: start stop test migrate venv install clean