from datetime import date as dt

from django.core.exceptions import ValidationError


def validate_date(value):
    difference = value - dt.today()
    if difference.days < 0:
        raise ValidationError("Date cannot be in the past")
