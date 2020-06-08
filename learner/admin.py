from django.contrib import admin

from learner.models import Question, User, Session


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email", "is_superuser", "date_joined", "last_login")
    # "username", "gender", "age", "mother_tongue", "other_language",


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "t", "item", "correct_reply", "new",
        "user_reply", "success",
        "time_display", "time_reply", "_possible_replies")

    @staticmethod
    def _possible_replies(obj):
        return ", ".join([p.meaning for p in obj.possible_replies.all()])

    @staticmethod
    def correct_reply(obj):

        return obj.kanji.meaning.meaning


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "date_creation", "available_time", "n_iteration", "close")


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Session, SessionAdmin)

