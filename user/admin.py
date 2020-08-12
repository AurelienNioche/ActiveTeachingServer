from django.contrib import admin

from user.models.user import User
from user.models.question import Question
from user.models.session import Session


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email", "is_superuser", "date_joined", "condition",
        "last_login", "gender", "age", "mother_tongue", "other_language")


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "item", "correct_reply", "new",
        "user_reply", "success",
        "time_display", "time_reply", "_possible_replies", "teaching_engine")

    @staticmethod
    def _possible_replies(obj):
        return ", ".join([p.meaning for p in obj.possible_replies.all()])

    @staticmethod
    def correct_reply(obj):

        return obj.kanji.meaning.meaning


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "date_creation", "available_time", "next_available_time",
        "n_iteration", "open", "is_evaluation", "teaching_engine")


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Session, SessionAdmin)