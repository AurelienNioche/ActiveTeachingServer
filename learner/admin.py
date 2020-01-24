from django.contrib import admin

# Register your models here.
from learner.models import Question, User
from teaching_material.models import Kanji

from core.task_parameters import N_POSSIBLE_REPLIES


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email", "is_superuser", "date_joined", "last_login")
    # "username", "gender", "age", "mother_tongue", "other_language",



class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "t", "kanji",
        "reply", "success",
        "time_display", "time_reply", "possible_replies")


    def possible_replies(self, obj):
        return "\n".join([p.meaning for p in obj.possible_replies.all()])

admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)

