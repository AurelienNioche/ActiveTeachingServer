from django.contrib import admin

from . models import Leitner
from . models.threshold import Threshold
from . models.psychologist import Psychologist
from . models.mcts import MCTSTeacher


# Register your models here.
class LeitnerAdmin(admin.ModelAdmin):
    list_display = (
        "user", "delay_factor", "_material",
        "n_item", "id_items", "box", "due")

    @staticmethod
    def _material(obj):
        return ", ".join([m.value for m in obj.material.all()])


class ThresholdAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Threshold._meta.fields ] + ["_material", ]

    @staticmethod
    def _material(obj):
        return ", ".join([m.value for m in obj.material.all()])


class MCTSAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MCTSTeacher._meta.fields] + ["_material", ]

    @staticmethod
    def _material(obj):
        return ", ".join([m.value for m in obj.material.all()])


class PsychologistAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Psychologist._meta.fields]



admin.site.register(Leitner, LeitnerAdmin)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(Psychologist, PsychologistAdmin)
admin.site.register(MCTSTeacher, MCTSAdmin)
