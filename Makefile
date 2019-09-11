BASEDIR=$(shell cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

ENV = $(BASEDIR)/.venv

PYBIN = $(ENV)/bin
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
ADMIN = $(PYBIN)/django-admin

PYTHON_PATH = $(BASEDIR)

SETTINGS_DEV_SQLITE = "config.settings.dev_sqlite"
SETTINGS_DEV_POSTGRES = "config.settings.dev_postgres"
SETTINGS_PRD = "config.settings.prd"

.PHONY: all
all:
	@echo "OK"

.PHONY: run
run: $(PYTHON) $(ADMIN)
	$(ADMIN) runserver --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE)

.PHONY: migrate
migrate: $(PYTHON) $(ADMIN)
	$(ADMIN) migrate --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE)

$(PYTHON):
	virtualenv .venv

$(ADMIN): $(PYTHON)
	$(PIP) install -r requirements.txt

.PHONY: docker_run
docker_run:
	docker-compose -f compose/dev.yml up --build -d

.PHONY: down
down:
	docker-compose -f compose/dev.yml down

.PHONY: css
css:
	yarn css-build

.PHONY: css_watch
css_watch:
	yarn css-watch
