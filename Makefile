BASEDIR=$(shell cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

ENV = $(BASEDIR)/.venv

PYBIN = $(ENV)/bin
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
ADMIN = $(PYBIN)/django-admin

PYTHON_PATH = $(BASEDIR)

SETTINGS_DEV_SQLITE = "config.settings.dev_sqlite"
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

.PHONY: collectstatic
collectstatic: $(PYTHON) $(ADMIN)
	echo ${DJANGO_SETTINGS_MODULE}
	python manage.py collectstatic --settings ${DJANGO_SETTINGS_MODULE}

$(PYTHON):
	virtualenv .venv

$(ADMIN): $(PYTHON)
	$(PIP) install -r requirements.txt

.PHONY: drun
drun:
	docker-compose -f compose/dev.yml up --build -d

.PHONY: prun
prun:
	docker-compose -f compose/production.yml up --build -d

.ONESHELL:
.PHONY: down
down:
	for env in production dev
	do
		if docker ps --format "table {{.Image}}" | grep $${env}_django
		then
			docker-compose -f compose/$${env}.yml down
		fi
	done

.PHONY: css
css:
	yarn css-build

.PHONY: css_watch
css_watch:
	yarn css-watch

.PHONY: database_url
database_url:
	@ echo "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
