from django.contrib import admin

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.mcts import MCTSTeacher
from teaching.models.teacher.sampling import Sampling

from teaching.models.psychologist.bayesian_grid import Psychologist

from teaching.models.learner.exp_decay import ExpDecay
from teaching.models.learner.walsh import Walsh2018

from teaching.models.teaching_engine import TeachingEngine


class TeachingEngineAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TeachingEngine._meta.fields] \
                   + ["_material", ]

    @staticmethod
    def _material(obj):
        return ", ".join([m.value for m in obj.material.all()])


class LeitnerAdmin(admin.ModelAdmin):
    list_display = (
        "delay_factor", "delay_min", "n_item", "box", "due")


class ThresholdAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Threshold._meta.fields]


class MCTSAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MCTSTeacher._meta.fields]


class SamplingAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Sampling._meta.fields]


class PsychologistAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Psychologist._meta.fields]


class ExpDecayAdmin(admin.ModelAdmin):

    list_display = [f.name for f in ExpDecay._meta.fields]


class WalshAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Walsh2018._meta.fields]


admin.site.register(Leitner, LeitnerAdmin)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(Psychologist, PsychologistAdmin)
admin.site.register(MCTSTeacher, MCTSAdmin)
admin.site.register(TeachingEngine, TeachingEngineAdmin)
admin.site.register(Sampling, SamplingAdmin)
admin.site.register(ExpDecay, ExpDecayAdmin)
admin.site.register(Walsh2018, WalshAdmin)
