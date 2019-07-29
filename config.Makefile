PYTHON_ONLY=1

HOST ?= misfile.l
SERVER_PORT ?= 9996
API_PORT = $(SERVER_PORT)

export SERVER = $(HOST):$(SERVER_PORT)
export FLASK_APP ?= $(PWD)/lib/backend/__init__.py
export FLASK_CONFIG ?= $(PWD)/lib/backend/application.cfg
export FLASK_TEST_CONFIG ?= $(PWD)/lib/backend/application-test.cfg
export FLASK_DEBUG ?= 1
export FLASK_ENV ?= development

# Python env
PYTHON_VERSION ?= python
PIPENV ?= $(shell command -v pipenv 2> /dev/null)
VENV = $(PWD)/.venv
export PIPENV_VENV_IN_PROJECT = 1


URL_TEST = https://misfile.test-$(CI_PROJECT_NAME)-$(BRANCH_NAME).kozea.fr
URL_PROD = https://misfile.kozea.fr
