from django.contrib import admin

from learner.models.user import User
from learner.models.question import Question


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email", "is_superuser", "date_joined", "condition",
        "last_login", "gender", "age", "mother_tongue", "other_language")


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "item", "correct_reply", "new",
        "user_reply", "success",
        "time_display", "time_reply", "_possible_replies")

    @staticmethod
    def _possible_replies(obj):
        return ", ".join([p.meaning for p in obj.possible_replies.all()])

    @staticmethod
    def user(obj):
        return obj.leitner.user

    @staticmethod
    def correct_reply(obj):

        return obj.kanji.meaning.meaning


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
