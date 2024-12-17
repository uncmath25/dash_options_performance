.PHONY: clean build-dev run-dev build-app flake-app test-app start-app stop-app build-prod start-prod stop-prod deploy

SHELL := /bin/bash

DEV_NAME := uncmath25/dash_options_performance_dev
APP_NAME := uncmath25/dash_options_performance_app
PROD_NAME := uncmath25/dash_options_performance_prod
DEV_RUN_NAME := dash_options_performance_dev
APP_RUN_NAME := dash_options_performance_app
PROD_RUN_NAME := dash_options_performance_prod

DEV_HOME_DIR := /home/jovyan

REMOTE_SERVER_PROFILE="testinglab"
REMOTE_PARENT_WEBSITE_DIR="/home/player1/websites/dash_options_performance"

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
		--env-file=.env \
		-e JUPYTER_ENABLE_LAB=yes \
		-p 8888:8888 \
		-v "$$(pwd)/notebooks:$(DEV_HOME_DIR)/notebooks" \
		-v "$$(pwd)/.ipython:$(DEV_HOME_DIR)/.ipython" \
		-v "$$(pwd)/.jupyter:$(DEV_HOME_DIR)/.jupyter" \
		-v "$$(pwd)/.local:$(DEV_HOME_DIR)/.local" \
		--name $(DEV_RUN_NAME) \
		$(DEV_NAME)

build-app: clean
	@echo "*** Building development dash app docker image ***"
	docker build -f Dockerfile-app -t $(APP_NAME) .

flake-app: build-app
	@echo "*** Linting repo ***"
	docker run --rm $(APP_NAME) bash -c "flake8 --ignore=E501,W503 /app"

test-app: flake-app
	@echo "*** Testing repo ***"
	docker run --rm -v "$$(pwd)/tests:/tests" $(APP_NAME):latest bash -c "pytest /tests"

start-app: test-app
	@echo "*** Starting dockerized development dash app ***"
	docker run \
		-d \
		--env-file .env \
		-p 5000:5000 \
		-v "$$(pwd)/src:/app" \
		--name $(APP_RUN_NAME) \
		$(APP_NAME)

stop-app:
	@echo "*** Stopping dockerized development dash app ***"
	docker rm -f $(APP_RUN_NAME)

build-prod: test-app
	@echo "*** Building production nginx uwsgi flask docker image ***"
	docker build -f Dockerfile-prod -t $(PROD_NAME) .

start-prod: build-prod
	@echo "*** Starting production nginx uwsgi flask docker container ***"
	docker run -d -p 8001:8001 --env-file .env --name $(PROD_RUN_NAME) $(PROD_NAME)

stop-prod:
	@echo "*** Stopping production nginx uwsgi flask docker container ***"
	docker rm -f $(PROD_RUN_NAME)

deploy:
	@echo "*** Deploying Dockerized flask dash app to DigitalOcean droplet... ***"
	docker build --platform=linux/x86_64 -t $(PROD_NAME) -f Dockerfile-prod .
	docker save $(PROD_NAME) | ssh -C $(REMOTE_SERVER_PROFILE) docker load
	ssh $(REMOTE_SERVER_PROFILE) rm -rf $(REMOTE_PARENT_WEBSITE_DIR)
	scp -r ./* $(REMOTE_SERVER_PROFILE):$(REMOTE_PARENT_WEBSITE_DIR)
	scp -r .env $(REMOTE_SERVER_PROFILE):$(REMOTE_PARENT_WEBSITE_DIR)
	ssh $(REMOTE_SERVER_PROFILE) "\
		cd $(REMOTE_PARENT_WEBSITE_DIR); \
		docker rm -f $(PROD_RUN_NAME); \
		docker run --rm -d --env-file=.env --network host --name $(PROD_RUN_NAME) $(PROD_NAME); \
	"
	@echo "*** Restart the remote server with _restart_server.sh ***"
