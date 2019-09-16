### Brief decsription

This project is based on the structure provided by the cookicutter django set
up. The root `urls.py` and project settings are contained in the `config`
directory. As this is only a test project, all the environment variables,
including secrets, have been commited to vs.

Requirements to get the project running: `docker`, `docker-compose` and `make`

Fingers crossed, this is all that is needed to test it:
    `make prun`
 
### Bugs

The way the event creation was handled turned out to be wonky, as the meat
choices are handled separately from the form, thus if the user inputs a wrong
date, the meats need to be rechosen. This architecture remained due to having
commited to it too much and having strayed too far from the light.

### Where are the tests?

They should be released with the rollout of the next version. Crunch time made
tests improbable.


#### Makefile commands:
* **run**: Run local server using sqlite
* **drun**: Run dockerized server using postgres with mounted project directory (develop run)
* **prun**: Run dockerized server using postgres, gunicorn and nginx
    (production run)
* **migrate**: Run local sqlite migrations
* **down**: Spin down containers
* **build**: Compile scss and js
* **watch**: Continuously build scss and js
