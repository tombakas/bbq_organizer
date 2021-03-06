FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  # build dependencies
  && apk add make yarn \
  # postgres
  && apk add postgresql-dev

RUN addgroup -S django \
    && adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

COPY . /opt/app/

RUN chown -R django /opt/app

RUN mkdir /staticfiles
RUN chown django /staticfiles
RUN chmod 755 /staticfiles

USER django

WORKDIR /opt/app
RUN export DATABASE_URL=$(make database_url)
RUN yarn install

ENTRYPOINT ["/entrypoint"]
