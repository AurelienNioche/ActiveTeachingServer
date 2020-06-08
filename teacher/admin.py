from django.contrib import admin

from . models import Leitner


# Register your models here.
class LeitnerAdmin(admin.ModelAdmin):
    list_display = (
        "user", "delay_factor", "_material",
        "n_item", "id_items", "box", "due")

    @staticmethod
    def _material(obj):
        return ", ".join([m.value for m in obj.material.all()])


admin.site.register(Leitner, LeitnerAdmin)
