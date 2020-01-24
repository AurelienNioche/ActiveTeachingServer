from django.db import models


class Meaning(models.Model):

    meaning = models.CharField(max_length=2555, blank=True, null=True)

    def __str__(self):
        return getattr(self, "meaning")

    class Meta:

        db_table = 'meaning'
        app_label = 'teaching_material'
