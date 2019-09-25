from datetime import datetime as dt
from datetime import timedelta as td

from django.contrib.auth.models import User
from django.core.validators import ValidationError
from django.test import TestCase

from bbq_organizer.models import Event


class PastDateValidator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bbq_user", password="secret")

    def test_date_in_past(self):
        yesterday = (dt.now() - td(days=1)).strftime("%Y-%m-%d")
        event = Event(date=yesterday, author=self.user)
        with self.assertRaises(ValidationError):
            event.full_clean()
