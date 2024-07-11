# --- Variables --------------------------------------------------------------------------------------------------------
include ./todo_list/.env
export MODE

MODE := $(MODE:"%"=%)
WORKDIR = ./todo_list
IMAGE = todo-list:latest
COMPOSE_FILE = $(WORKDIR)/docker-compose.yml


# --- Docker -----------------------------------------------------------------------------------------------------------
.PHONY: build rebuild destroy up stop down down-v logs

rebuild: down destroy build

build:
	docker build -t $(IMAGE) $(WORKDIR) --target $(MODE)

destroy:
	docker rmi -f $(IMAGE)

up:
	docker compose -f $(COMPOSE_FILE) up -d

stop:
	docker compose -f $(COMPOSE_FILE) stop

down:
	docker compose -f $(COMPOSE_FILE) down

down-v:
	docker compose -f $(COMPOSE_FILE) down -v

logs:
	docker compose -f $(COMPOSE_FILE) logs -f


# --- Django -----------------------------------------------------------------------------------------------------
.PHONY: migrations migrate create-superuser

migrations:
	cd $(WORKDIR) && poetry run python manage.py makemigrations

migrate:
	docker compose -f $(COMPOSE_FILE) run --rm todo-list python manage.py migrate

create-superuser: up
	docker exec -it todo-list python manage.py createsuperuser


# --- Code Linters -----------------------------------------------------------------------------------------------------
.PHONY: lint flake8

lint: flake8

flake8:
	@echo Starting flake8...
	cd $(WORKDIR) && poetry run flake8 --toml-config=pyproject.toml .
	@echo All done! ✨ 🍰 ✨


# --- Code Formatters --------------------------------------------------------------------------------------------------
.PHONY: reformat isort black

reformat: isort black

isort:
	@echo Starting isort...
	cd $(WORKDIR) && poetry run isort --settings=pyproject.toml .

black:
	@echo Starting black...
	cd $(WORKDIR) && poetry run black --config=pyproject.toml .