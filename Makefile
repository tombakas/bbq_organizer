BASEDIR=$(shell cd "$( dirname "${BASH_SOURCE[0]}"   )" && pwd   )

ENV = $(BASEDIR)/../.venv

PYBIN = $(ENV)/bin
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
ADMIN = $(PYBIN)/django-admin

PYTHON_PATH = $(BASEDIR)
SETTINGS_DEV = "config.settings"

.PHONY: all
all:
	@echo "OK"

.PHONY: run
run:
	$(ADMIN) runserver --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV)
