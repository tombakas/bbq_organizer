BASEDIR=$(shell cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

ENV = $(BASEDIR)/.venv

PYBIN = $(ENV)/bin
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
ADMIN = $(PYBIN)/django-admin

PYTHON_PATH = $(BASEDIR)

SETTINGS_DEV = "config.settings.dev"
SETTINGS_PRD = "config.settings.prd"

.PHONY: all
all:
	@echo "OK"

.PHONY: run
run: $(PYTHON) $(ADMIN)
	$(ADMIN) runserver --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV)

.PHONY: migrate
migrate: $(PYTHON) $(ADMIN)
	$(ADMIN) migrate --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV)

$(PYTHON):
	virtualenv .venv

$(ADMIN): $(PYTHON)
	$(PIP) install -r requirements.txt
