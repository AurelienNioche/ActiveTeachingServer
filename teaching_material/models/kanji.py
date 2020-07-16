from django.db import models

from . meaning import Meaning


# Create your models here.
class Kanji(models.Model):

    value = models.TextField()  # Field name made lowercase.
    meaning = models.ForeignKey(Meaning, on_delete=models.CASCADE)

    class Meta:

        db_table = 'kanji'
        app_label = 'teaching_material'

    def __str__(self):
        return getattr(self, "kanji")
