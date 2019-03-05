from django.contrib import admin

# Register your models here.
from . models import User, Question, Kanji


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "registration_time")  # "username", "gender", "age", "mother_tongue", "other_language",


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_id", "t", "question", "reply")


class KanjiAdmin(admin.ModelAdmin):
    list_display = (
        "id", "kanji", "meaning", "translation_of_on", "translation_of_kun")
    # , "reading_within_joyo", "reading_beyond_joyo")


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Kanji, KanjiAdmin)
