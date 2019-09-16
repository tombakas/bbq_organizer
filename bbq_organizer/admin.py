from django.contrib import admin

from bbq_organizer.models import Event
from bbq_organizer.models import MeatChoice
from bbq_organizer.models import MeatType


class EventAdmin(admin.ModelAdmin):
    pass


class MeatChoiceAdmin(admin.ModelAdmin):
    pass


class MeatTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(MeatChoice, MeatChoiceAdmin)
admin.site.register(MeatType, MeatTypeAdmin)
