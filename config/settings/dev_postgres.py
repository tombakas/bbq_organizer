from .base import * # noqa
from .base import env

SECRET_KEY = "fgtj2pic#t92)4gq$%e1%k!&r$&d=0)2s4sb^&8&m01q1hju(&"
DEBUG = True

DATABASES = {"default": env.db("DATABASE_URL")}
