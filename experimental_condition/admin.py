from django.contrib import admin

from experimental_condition.models.pilot import Pilot
from experimental_condition.models.test_leitner import TestLeitner
from experimental_condition.models.test_active import TestActive
from experimental_condition.models.experiment import \
    RecursiveCondition, ThresholdCondition


class TestActiveAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TestActive._meta.fields]


class TestLeitnerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TestLeitner._meta.fields]


class PilotAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Pilot._meta.fields]


class RecursiveConditionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in RecursiveCondition._meta.fields]


class ThresholdConditionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ThresholdCondition._meta.fields]


admin.site.register(TestActive, TestActiveAdmin)
admin.site.register(TestLeitner, TestLeitnerAdmin)
admin.site.register(Pilot, PilotAdmin)
admin.site.register(RecursiveCondition, RecursiveConditionAdmin)
admin.site.register(ThresholdCondition, ThresholdConditionAdmin)
