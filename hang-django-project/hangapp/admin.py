from django.contrib import admin

from .models import Decision, Option, User, Session

admin.site.register(Decision)
admin.site.register(Option)
admin.site.register(User)
admin.site.register(Session)