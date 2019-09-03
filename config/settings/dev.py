import os

from .base import * # noqa

SECRET_KEY = 'fgtj2pic#t92)4gq$%e1%k!&r$&d=0)2s4sb^&8&m01q1hju(&'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # noqa:F405
    }
}
