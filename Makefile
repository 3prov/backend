DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml

DOCKER_COMPOSE=docker-compose
DOCKER_BUILDKIT_FLAG=1

.PHONY: up_prod up_dev build_dev build_prod connect_to_backend_dev \
		connect_to_backend_prod test_dev test_prod clean_dev fclean_dev logs_prod \
		dev prod

# PRODUCTION
prod: build_prod up_prod test_prod logs_prod

build_prod:
	DOCKER_BUILDKIT=$(DOCKER_BUILDKIT_FLAG) $(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_PROD_FILE) build

up_prod:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_PROD_FILE) up -d

logs_prod:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_PROD_FILE) logs -f

connect_to_backend_prod:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_PROD_FILE) exec backend sh

test_prod:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_PROD_FILE) exec backend sh -c "coverage run --omit=*/tests* manage.py test --no-input && coverage report"

# DEVELOPMENT
dev: build_dev up_dev

build_dev:
	DOCKER_BUILDKIT=$(DOCKER_BUILDKIT_FLAG) $(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) build

up_dev:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) up -d

logs_dev:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) logs -f

connect_to_backend_dev:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) exec backend sh

test_dev:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) exec backend sh -c "coverage run --omit=*/tests* manage.py test --no-input && coverage report"

# DELETES ALL CONTAINERS AND IMAGES
clean_dev:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) down

# DELETES ALL CONTAINERS AND IMAGES WITH VOLUMES
fclean_dev:
	$(DOCKER_COMPOSE) --file=$(DOCKER_COMPOSE_DEV_FILE) down -v
