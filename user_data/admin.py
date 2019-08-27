from django.contrib import admin

# Register your models here.
from user_data.models import Question, User
from teaching_material.models import Kanji

from task.fixed_parameters import N_POSSIBLE_REPLIES


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "registration_time")
    # "username", "gender", "age", "mother_tongue", "other_language",


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "user_id", "t", "question", "reply", "success",
        "time_display", "time_reply", "possible_replies")


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)

