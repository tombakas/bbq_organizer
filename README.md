### Brief description

This project is based on the structure provided by the cookicutter django set up. The root `urls.py` and project settings are contained in the `config` directory. As this is only a test project, all the environment variables, including secrets, have been commited to vc. The static assets are compiled using webpack. There are three setups: two for development and one for production (faux-duction). For running **development**, the dependencies in **package.json** need to be installed locally by running either `npm install` or `yarn install`. This makes the `make build`, `make dev_build`, `make watch` and `make dev_watch` commands available.

* The simplest setup just uses sqlite and a local django development server, it can be launched by running `make run` and then in parallel running `make watch` to compile static assets.
* Then there is a dockerized setup that still mounts the local directory and thus expects for the static files to be compiled locally. It can be run with `make drun`
* Finally, the faux-production setup partly immitates what a production environment looks like and copies over all the assets and compiles them autonomously. It can be run with `make prun`.

**Requirements** to get the project running: `docker`, `docker-compose` and `make`

Fingers crossed, this is all that is needed to run it:
    `make prun`

The _production_ setup maps to port **8123** by default. The password validator
is very picky in _production_, which can be circumvented for testing by setting
`AUTH_PASSWORD_VALIDATORS=[]` in `config/settings/production.py`.

### Dev maintenance

Tu be run on first deployment and when needed:

* Applying database migrations: `make migrate`
* Populating database with data fixtures: `make data`
* Compiling css and js: `make build`
* Compiling css and js continuously: `make watch`
* Running tests: `make test`

 
### Tests

The project currently has 100% test coverage:
![Test coverage](https://i.imgur.com/wlQtHiN.png)

### Makefile commands:
* **run**: Run local server using sqlite
* **drun**: Run dockerized server using postgres with mounted project directory (develop run)
* **prun**: Run dockerized server using postgres, gunicorn and nginx
    (production run)
* **migrate**: Run local sqlite migrations
* **data**: Populate db with data fixtures
* **superuser**: Create superuser
* **down**: Spin down containers
* **build**: Compile scss and js
* **watch**: Continuously build scss and js

### Original project spec

#### BBQ planner functional requirements:

**Creating a BBQ event**
* A BBQ event organizer needs to be able to register and login
* Create a new BBQ event
* Be able to set a date for a BBQ event
* Be able to register types of meat you want to serve during the BBQ
* Each BBQ event has a public link, which you can share with your friends to let them register for the event

**BBQ event visitors**
* Can register for an event without an account using the public shared link of the BBQ event organizer
* When registering, the visitor needs to enter his name.
* When registering, the visitor can select how many guests he will bring.
* When registering, the visitor can select how many types of which meat he wants. The list of meat shown is configured by the BBQ organizer.

#### BBQ event summary / shopping list

A logged in BBQ event organizer can an overview of his BBQ events.

**Per BBQ event, the organizer sees**
* How many people have registered in total (sum of visitors + guests).
* Per type of meat, how many people would like a piece
* List of all the names of visitors who have registered
