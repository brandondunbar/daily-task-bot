# ====== Config ======
APP_NAME        ?= daily-task-bot
IMAGE           ?= $(APP_NAME)
TAG             ?= dev
FULL_IMAGE      ?= $(IMAGE):$(TAG)
CONTAINER_NAME  ?= $(APP_NAME)
PLATFORM        ?= linux/amd64

# Optional env file for docker run
ENV_FILE        ?= .env
USE_ENV_FILE    := $(shell [ -f $(ENV_FILE) ] && echo 1 || echo 0)

# Timezone
TZ              ?= America/New_York

DOCKER          ?= docker
DOCKER_BUILDKIT ?= 1

# Common run flags
RUN_FLAGS_BASE  := --rm --name $(CONTAINER_NAME)
RUN_FLAGS_ENV   := -e TZ=$(TZ)
ifeq ($(USE_ENV_FILE),1)
	RUN_FLAGS_ENV += --env-file $(ENV_FILE)
endif

# ====== Phony targets ======
.PHONY: help build buildx run run-bg stop logs sh ps rm rmi clean \
        test lint fmt freeze deps-compile deps-upgrade check-env

# ====== Help ======
help:
	@echo "Targets:"
	@echo "  build          Build the image ($(FULL_IMAGE))"
	@echo "  buildx         Build with buildx for $(PLATFORM)"
	@echo "  run            Run in foreground (Ctrl+C or 'make stop' to exit)"
	@echo "  run-bg         Run detached (background)"
	@echo "  stop           Stop the running container"
	@echo "  logs           Follow logs"
	@echo "  sh             Shell into a fresh container (bash)"
	@echo "  ps             Show container status"
	@echo "  rm             Remove stopped container"
	@echo "  rmi            Remove image"
	@echo "  clean          Remove container and image"
	@echo "  test           Run pytest inside container"
	@echo "  lint           Run ruff lint inside container"
	@echo "  fmt            Run black format inside container"
	@echo "  freeze         Freeze current deps from a local venv to requirements.txt"
	@echo "  deps-compile   Use pip-tools to compile pins into requirements.txt"
	@echo "  deps-upgrade   Upgrade pins with pip-tools (backtracking resolver)"
	@echo ""
	@echo "Variables (override like: make build TAG=prod):"
	@echo "  IMAGE, TAG, CONTAINER_NAME, ENV_FILE, TZ, PLATFORM"

# ====== Build ======
build:
	@echo ">> Building $(FULL_IMAGE)"
	@DOCKER_BUILDKIT=$(DOCKER_BUILDKIT) $(DOCKER) build -t $(FULL_IMAGE) .

buildx:
	@echo ">> Building (buildx) $(FULL_IMAGE) for $(PLATFORM)"
	@$(DOCKER) buildx build --platform $(PLATFORM) -t $(FULL_IMAGE) .

# ====== Run & Manage ======
run: check-env
	@echo ">> Running $(FULL_IMAGE) as $(CONTAINER_NAME)"
	@$(DOCKER) run $(RUN_FLAGS_BASE) $(RUN_FLAGS_ENV) $(FULL_IMAGE)

run-bg: check-env
	@echo ">> Running (detached) $(FULL_IMAGE) as $(CONTAINER_NAME)"
	@$(DOCKER) run -d $(RUN_FLAGS_BASE) $(RUN_FLAGS_ENV) $(FULL_IMAGE)

stop:
	@echo ">> Stopping $(CONTAINER_NAME)"
	-@$(DOCKER) stop $(CONTAINER_NAME) >/dev/null 2>&1 || true

logs:
	@$(DOCKER) logs -f $(CONTAINER_NAME)

sh:
	@echo ">> Starting shell in fresh container"
	@$(DOCKER) run --rm -it $(RUN_FLAGS_ENV) $(FULL_IMAGE) bash || /bin/sh

ps:
	@$(DOCKER) ps -a --filter "name=$(CONTAINER_NAME)"

rm:
	@echo ">> Removing container $(CONTAINER_NAME) if exists"
	-@$(DOCKER) rm -f $(CONTAINER_NAME) >/dev/null 2>&1 || true

rmi:
	@echo ">> Removing image $(FULL_IMAGE) if exists"
	-@$(DOCKER) rmi $(FULL_IMAGE) >/dev/null 2>&1 || true

clean: stop rm rmi
	@echo ">> Clean complete"

# ====== Dev: tests & tooling (inside container) ======
test:
	@echo ">> Running pytest in container"
	@$(DOCKER) run --rm $(RUN_FLAGS_ENV) $(FULL_IMAGE) pytest -q

lint:
	@echo ">> Running ruff in container"
	@$(DOCKER) run --rm $(RUN_FLAGS_ENV) $(FULL_IMAGE) ruff check .

fmt:
	@echo ">> Running black in container"
	@$(DOCKER) run --rm $(RUN_FLAGS_ENV) $(FULL_IMAGE) black .

# ====== Dependencies management ======
freeze:
	@echo ">> Freezing currently installed packages into requirements.txt"
	@pip freeze > requirements.txt

deps-compile:
	@echo ">> Compiling requirements.txt from requirements.in with pip-tools"
	@python -m pip install --upgrade pip pip-tools >/dev/null
	@pip-compile --generate-hashes -o requirements.txt requirements.in

deps-upgrade:
	@echo ">> Upgrading pins with pip-tools (backtracking resolver)"
	@python -m pip install --upgrade pip pip-tools >/dev/null
	@pip-compile --upgrade --resolver=backtracking --generate-hashes -o requirements.txt requirements.in

# ====== Utilities ======
check-env:
ifeq ($(USE_ENV_FILE),0)
	@echo ">> Note: $(ENV_FILE) not found; continuing without --env-file"
endif
	@true
