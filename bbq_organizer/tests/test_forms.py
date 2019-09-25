from datetime import datetime as dt
from datetime import timedelta as td

from django.test import TestCase

from bbq_organizer.forms import EventForm


class TestEventForm(TestCase):
    def test_form_valid(self):
        today = dt.now().strftime("%Y-%m-%d")
        form_data = {"date": today}
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_malformed_date(self):
        today_wrong = dt.now().strftime("%Y-%m")
        form_data = {"date": today_wrong}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
