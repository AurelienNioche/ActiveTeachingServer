from django.contrib import admin

from experimental_condition.models.session import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "date_creation", "available_time", "n_iteration", "close")


admin.site.register(Session, SessionAdmin)
