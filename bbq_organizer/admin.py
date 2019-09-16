from django.contrib import admin

from bbq_organizer.models import Event
from bbq_organizer.models import MeatChoice


class EventAdmin(admin.ModelAdmin):
    pass


class MeatChoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(MeatChoice, MeatChoiceAdmin)
