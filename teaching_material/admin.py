from django.contrib import admin

from teaching_material.models import Kanji, Finnish


# Kanji custom admin
class KanjiAdmin(admin.ModelAdmin):
    list_display = (
        "id", "index", "kanji", "meaning",
        "translation_of_on", "translation_of_kun",
        "grade", "strokes")
    # , "reading_within_joyo", "reading_beyond_joyo")

# Register your models here.
admin.site.register(Kanji, KanjiAdmin)
admin.site.register(Finnish)
