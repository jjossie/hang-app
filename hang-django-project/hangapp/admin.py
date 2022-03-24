from django.contrib import admin

from .models import Decision, Option, Homie, Session

admin.site.register(Decision)
admin.site.register(Option)
admin.site.register(Homie)
admin.site.register(Session)