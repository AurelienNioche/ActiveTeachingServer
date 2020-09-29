from django.contrib import admin

import numpy as np

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.sampling import Sampling
from teaching.models.teacher.recursive import Recursive
from teaching.models.teacher.forward import Forward
from teaching.models.teacher.evaluator import Evaluator

from teaching.models.psychologist.bayesian_grid \
    import Psychologist, Param, LogPost

from teaching.models.learner.exp_decay import ExpDecay
from teaching.models.learner.walsh import Walsh2018

from teaching.models.teaching_engine import TeachingEngine


class TeachingEngineAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TeachingEngine._meta.fields
                    if f.name not in ("id_items", )] \
                   + ["view_material", ]

    @staticmethod
    def view_material(obj):
        characters = [obj.material.get(id=id_).value for id_ in obj.id_items]
        return ", ".join(characters[:3]) + ", ... , " + ", ".join(characters[-3:])


class LeitnerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Leitner._meta.fields
                    if f.name not in ("box", "due", )] + ["view_box", "view_due"]

    def view_box(self, obj):
        return f"{obj.box[0]}, {obj.box[1]}, ... , {obj.box[-2]}, {obj.box[-1]}"

    def view_due(self, obj):
        return f"{obj.due[0]}, {obj.due[1]}, ... , {obj.due[-2]}, {obj.due[-1]}"


class ThresholdAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Threshold._meta.fields]


class SamplingAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Sampling._meta.fields]


class RecursiveAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Recursive._meta.fields]


class ForwardAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Forward._meta.fields]


class PsychologistAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Psychologist._meta.fields
                    if f.name not in ("grid_param", "n_pres")] \
                   + ["view_bounds", "view_grid_param", "view_n_pres"]

    def view_grid_param(self, obj):
        gp = np.reshape(obj.grid_param, (-1, obj.n_param))
        return f"{gp[0]}, {gp[1]}, ... , " \
               f"{gp[-2]}, {gp[-1]}"

    def view_n_pres(self, obj):
        return f"{obj.n_pres[0]}, {obj.n_pres[1]}, {obj.n_pres[2]}, ... , " \
               f"{obj.n_pres[-2]}, {obj.n_pres[-1]}"

    def view_bounds(self, obj):
        gp = np.reshape(obj.grid_param, (-1, obj.n_param))
        bounds = np.vstack((gp[0], gp[-1])).T
        return ", ".join((f"{b}" for b in bounds))


class ExpDecayAdmin(admin.ModelAdmin):

    list_display = [f.name for f in ExpDecay._meta.fields
                    if f.name not in ("seen", "seen_item", "n_pres",
                                      "last_pres", "ts", "hist")] \
                   + ["view_n_pres", ]

    def view_n_pres(self, obj):
        return f"{obj.n_pres[0]}, {obj.n_pres[1]}, {obj.n_pres[2]}, ... , " \
               f"{obj.n_pres[-2]}, {obj.n_pres[-1]}"


class WalshAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Walsh2018._meta.fields]


class EvaluatorAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Evaluator._meta.fields
                    if f.name not in ("seen", "evaluation_schedule")] \
                   + ["view_n_seen", ]

    def view_n_seen(self, obj):
        return f'{np.sum(obj.seen)}'


class ParamAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Param._meta.fields]


class LogPostAdmin(admin.ModelAdmin):

    list_display = [f.name for f in LogPost._meta.fields
                    if f.name not in ("value", )] + ["view_value"]

    def view_value(self, obj):
        return f"{obj.value[0]}, {obj.value[1]}, ... , " \
               f"{obj.value[-2]}, {obj.value[-1]}"


admin.site.register(LogPost, LogPostAdmin)
admin.site.register(Param, ParamAdmin)

admin.site.register(TeachingEngine, TeachingEngineAdmin)

admin.site.register(Psychologist, PsychologistAdmin)

admin.site.register(Leitner, LeitnerAdmin)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(Sampling, SamplingAdmin)
admin.site.register(Recursive, RecursiveAdmin)
admin.site.register(Forward, ForwardAdmin)

admin.site.register(ExpDecay, ExpDecayAdmin)
admin.site.register(Walsh2018, WalshAdmin)

admin.site.register(Evaluator, EvaluatorAdmin)
