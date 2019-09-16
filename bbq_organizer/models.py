import uuid

from django.db import models
from django.contrib.auth.models import User

from bbq_organizer.validators import validate_date


SLUG_LENGTH = 8


class Event(models.Model):
    date = models.DateField(validators=[validate_date])
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=SLUG_LENGTH, unique=True, null=False, blank=True)

    def __str__(self):
        return "{} | {} | {}".format(
            self.date.strftime("%Y %m %d"),
            self.author,
            self.id)

    @staticmethod
    def _generate_slug():
        # The potential for disaster should be minimal here
        while True:
            slug = uuid.uuid4().hex[:SLUG_LENGTH]
            if not Event.objects.filter(slug=slug).exists():
                break
        return slug

    def save(self, *args, **kwargs):
        self.slug = self._generate_slug()
        super().save(*args, **kwargs)
        return self


class MeatType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class SignUp(models.Model):
    name = models.CharField(max_length=64, blank=True)
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    extras = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self


class MeatOption(models.Model):
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    meat = models.ForeignKey(MeatType, null=False, on_delete=models.CASCADE)


class MeatChoice(models.Model):
    signup = models.ForeignKey(SignUp, null=False, on_delete=models.CASCADE)
    meat = models.ForeignKey(MeatType, null=False, on_delete=models.CASCADE)
