from django.contrib import admin

# Register your models here.
from . models import User, Data, Kanjilist


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "username", "gender", "age", "mother_tongue", "other_language", "registration_time")


class DataAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_id", "t", "question", "reply")


class KanjiAdmin(admin.ModelAdmin):
    list_display = (
        "id", "kanji", "meaning")
    # "translation_of_on", "translation_of_kun", "reading_within_joyo", "reading_beyond_joyo")


admin.site.register(User, UserAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Kanjilist, KanjiAdmin)
