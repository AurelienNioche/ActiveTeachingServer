from django.contrib import admin

from . models import Kanji, Meaning, WaniKani


class WaniKaniAdmin(admin.ModelAdmin):

    list_display = ["level", "character", "meaning",
                    "onyomi", "kunyomi", "nanori"]


class KanjiAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "meaning")


class MeaningAdmin(admin.ModelAdmin):
    list_display = ("id", "meaning")


admin.site.register(Kanji, KanjiAdmin)
admin.site.register(Meaning, MeaningAdmin)
admin.site.register(WaniKani, WaniKaniAdmin)
