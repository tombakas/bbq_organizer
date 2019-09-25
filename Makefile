BASEDIR=$(shell cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

ENV = $(BASEDIR)/.venv

PYBIN = $(ENV)/bin
PYTHON = $(PYBIN)/python
PIP = $(PYBIN)/pip
ADMIN = $(PYBIN)/django-admin

PYTHON_PATH = $(BASEDIR)

SETTINGS_DEV_SQLITE = "config.settings.dev_sqlite"
SETTINGS_TEST = "config.settings.test"

DJANGO_CONTAINER = \
	$(shell awk '/^  [a-z]/{django=0}/django:/{django=1}/container_name/{if(django){print $$2}}' compose/dev.yml)

.PHONY: all
all:
	echo $(DJANGO_CONTAINER)
	@echo "OK"

.PHONY: run
run: $(PYTHON) $(ADMIN)
	$(ADMIN) runserver --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE)

.ONESHELL:
.PHONY: migrate
migrate:
	@ if docker ps --format "table {{.Image}}" | grep $(DJANGO_CONTAINER)
	@ then
		docker exec $(DJANGO_CONTAINER) sh -c 'export DATABASE_URL=$$(make database_url); django-admin migrate'
	@ else
		$(MAKE) _lmigrate
	@ fi

.PHONY: _lmigrate
_lmigrate: $(PYTHON) $(ADMIN)
	$(ADMIN) migrate --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE)

.PHONY: test
test: $(PYTHON) $(ADMIN)
	$(ADMIN) test --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_TEST)

.PHONY: data
data:
	@ if docker ps --format "table {{.Image}}" | grep $(DJANGO_CONTAINER)
	@ then
		docker exec $(DJANGO_CONTAINER) sh -c 'export DATABASE_URL=$$(make database_url); django-admin loaddata meats.json'
	@ else
		$(MAKE) _ldata
	@ fi

.PHONY: _ldata
_ldata: $(PYTHON) $(ADMIN)
	$(ADMIN) loaddata --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE) meats.json

.PHONY: superuser
superuser:
	@ if docker ps --format "table {{.Image}}" | grep $(DJANGO_CONTAINER)
	@ then
		docker exec -it $(DJANGO_CONTAINER) sh -c 'export DATABASE_URL=$$(make database_url); django-admin createsuperuser'
	@ else
		$(MAKE) _lsuperuser
	@ fi

.PHONY: _lsuperuser
_lsuperuser: $(PYTHON) $(ADMIN)
	$(ADMIN) createsuperuser --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE)

.PHONY: makemigrations
makemigrations: $(PYTHON) $(ADMIN)
	$(ADMIN) makemigrations --pythonpath $(PYTHON_PATH) --settings $(SETTINGS_DEV_SQLITE) bbq_organizer

.PHONY: collectstatic
collectstatic: $(PYTHON) $(ADMIN)
	python manage.py collectstatic --settings ${DJANGO_SETTINGS_MODULE}

$(PYTHON):
	virtualenv -p $$(which python3) .venv

$(ADMIN): $(PYTHON)
	$(PIP) install -r requirements/base.txt

.PHONY: drun
drun:
	docker-compose -f compose/dev.yml up --build -d

.PHONY: prun
prun:
	docker-compose -f compose/production.yml up --build -d

.ONESHELL:
.PHONY: down
down:
	@ for env in production dev
	@ do
	@ 	if docker ps --format "table {{.Image}}" | grep $${env}_django
	@ 	then
	@ 		docker-compose -f compose/$${env}.yml down
	@ 	fi
	@ done

.PHONY: build
build:
	yarn build

.PHONY: watch
watch:
	yarn watch

.PHONY: dev_watch
dev_watch:
	yarn dev-watch

.PHONY: database_url
database_url:
	@ echo "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
