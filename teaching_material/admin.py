from django.contrib import admin

from . models import Kanji


# Register your models here.
class KanjiAdmin(admin.ModelAdmin):
    list_display = (
        "id", "index", "kanji", "meaning",
        "translation_of_on", "translation_of_kun",
        "grade", "strokes")
    # , "reading_within_joyo", "reading_beyond_joyo")


admin.site.register(Kanji, KanjiAdmin)
