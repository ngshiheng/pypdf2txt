NAME := pypdf2txt
SHELL=/bin/bash
POETRY := $(shell command -v poetry 2> /dev/null)
PYTHON := $(shell command -v python3 2> /dev/null)
DOCKER := $(shell command -v docker 2> /dev/null)
MAKEFLAGS += --no-print-directory
ENVIRONMENT ?= development

.DEFAULT_GOAL := help
##@ Helper
.PHONY: help
help:	## display this help message.
	@awk 'BEGIN {FS = ":.*##"; printf "Use make \033[36m<target>\033[0m where \033[36m<target>\033[0m is one of:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


##@ Usage
.PHONY: setup
setup:	## install packages and prepare environment with poetry.
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	@$(POETRY) install
	@$(POETRY) run pre-commit install
	@$(POETRY) shell

.PHONY: lint
lint:	## run the code linters with pre-commit.
	@$(POETRY) run pre-commit

.PHONY: run
run:	## run server
	@$(POETRY) run python3 main.py


##@ Docker
PHONY: build-docker
build-docker:	## build docker image.
	$(DOCKER) build -t $(NAME) . --build-arg ENVIRONMENT=$(ENVIRONMENT) -f docker/Dockerfile

.PHONY: run-docker
run-docker:	## run local development server in docker.
	@$(DOCKER) stop $(NAME) || true && $(DOCKER) rm $(NAME) || true
	$(DOCKER) run -d -p 8080:8080 --name $(NAME) $(NAME)
