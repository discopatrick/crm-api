# crm-api

## To run:

* Set an environment variable for your db, e.g.: `DATABASE_FILENAME=crm.sqlite`
* In a python terminal, initialise the db with:
  ```
  from crm.database import init_db
  init_db()
  ```
* Run redis with `docker run -d -p 6379:6379 redis`
* Run celery with `celery -A tasks worker --loglevel=info -B` (remember to add `-B` so celerybeat also runs)
* Set `FLASK_APP=crm`
* Run `python -m flask run`

## To test:

* Set an alternate env var for your db, e.g.: `DATABASE_FILENAME=test.sqlite`
* Run `python -m pytest`
