from .base import * # noqa
from .base import env

SECRET_KEY = env("DJANGO_SECRET_KEY")
STATIC_ROOT = env("STATIC_ROOT")
DEBUG = env("DEBUG")

DATABASES = {"default": env.db("DATABASE_URL")}
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
