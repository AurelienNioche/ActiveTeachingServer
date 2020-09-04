from django.contrib import admin

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.sampling import Sampling
from teaching.models.teacher.recursive import Recursive
from teaching.models.teacher.evaluator import Evaluator

from teaching.models.psychologist.bayesian_grid \
    import Psychologist, Param, LogPost

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
    list_display = [f.name for f in Leitner._meta.fields]
        # ("delay_factor", "delay_min", "n_item", "box", "due")


class ThresholdAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Threshold._meta.fields]


class SamplingAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Sampling._meta.fields]


class RecursiveAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Recursive._meta.fields]


class PsychologistAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Psychologist._meta.fields]


class ExpDecayAdmin(admin.ModelAdmin):

    list_display = [f.name for f in ExpDecay._meta.fields]


class WalshAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Walsh2018._meta.fields]


class EvaluatorAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Evaluator._meta.fields]


class ParamAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Param._meta.fields]


class LogPostAdmin(admin.ModelAdmin):

    list_display = [f.name for f in LogPost._meta.fields]


admin.site.register(LogPost, LogPostAdmin)

admin.site.register(Param, ParamAdmin)

admin.site.register(TeachingEngine, TeachingEngineAdmin)

admin.site.register(Psychologist, PsychologistAdmin)

admin.site.register(Leitner, LeitnerAdmin)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(Sampling, SamplingAdmin)
admin.site.register(Recursive, RecursiveAdmin)

admin.site.register(ExpDecay, ExpDecayAdmin)
admin.site.register(Walsh2018, WalshAdmin)

admin.site.register(Evaluator, EvaluatorAdmin)

# from teaching.models.teacher.mcts import MCTSTeacher
# class MCTSAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in MCTSTeacher._meta.fields]

# admin.site.register(MCTSTeacher, MCTSAdmin)
