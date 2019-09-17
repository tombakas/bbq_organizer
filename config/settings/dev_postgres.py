from .base import * # noqa
from .base import env

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

DATABASES = {"default": env.db("DATABASE_URL")}
AUTH_PASSWORD_VALIDATORS = env("AUTH_PASSWORD_VALIDATORS", default=[])
