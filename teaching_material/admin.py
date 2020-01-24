from django.contrib import admin

from . models import Kanji, Meaning


# Register your models here.
class KanjiAdmin(admin.ModelAdmin):
    list_display = (
        "id", "kanji", "meaning", "meaning_string",
        "translation_of_on", "translation_of_kun",
        "grade", "strokes")
    # , "reading_within_joyo", "reading_beyond_joyo")


class MeaningAdmin(admin.ModelAdmin):
    list_display = (
        "id", "meaning")
    # , "reading_within_joyo", "reading_beyond_joyo")


admin.site.register(Kanji, KanjiAdmin)
admin.site.register(Meaning, MeaningAdmin)
