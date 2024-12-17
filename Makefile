.PHONY: clean build-dev run-dev

SHELL := /bin/bash

DEV_NAME := uncmath25/dash_options_performance_dev
DEV_RUN_NAME := dash_options_performance_dev

DEV_HOME_DIR := /home/jovyan

default: run-dev

clean:
	@echo "*** Cleaning repo ***"
	mkdir -p .ipython
	mkdir -p .jupyter
	mkdir -p .local
	find . -name '__pycache__' -type d | xargs rm -rf
	find . -name '.pytest_cache' -type d | xargs rm -rf

build-dev: clean
	@echo "*** Building development jupyter docker image ***"
	docker build -f Dockerfile-dev -t $(DEV_NAME) .

run-dev: build-dev
	@echo "*** Running development jupyter server ***"
	docker run \
		--rm \
		--env-file=.env.dev \
		-e JUPYTER_ENABLE_LAB=yes \
		-p 8888:8888 \
		-v "$$(pwd)/notebooks:$(DEV_HOME_DIR)/notebooks" \
		-v "$$(pwd)/.ipython:$(DEV_HOME_DIR)/.ipython" \
		-v "$$(pwd)/.jupyter:$(DEV_HOME_DIR)/.jupyter" \
		-v "$$(pwd)/.local:$(DEV_HOME_DIR)/.local" \
		--name $(DEV_RUN_NAME) \
		$(DEV_NAME)
