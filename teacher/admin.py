from django.contrib import admin

from . models import Leitner


# Register your models here.
class LeitnerAdmin(admin.ModelAdmin):
    list_display = (
        "user", "delay_factor", "n_item",
        "taboo", "waiting_time", "box")


admin.site.register(Leitner, LeitnerAdmin)
