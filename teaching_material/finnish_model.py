from django.db import models

class Finnish(models.Model):
    # Automatic primary ID is added: https://docs.djangoproject.com/en/3.0/topics/db/models/#automatic-primary-key-fields  # noqa
    # id = models.AutoField(primary_key=True)
    # Lentokonesuihkuturbiinimoottoriapumekaanikkoaliupseerioppilas, longest Finnish word, is only 61 chars long
    word = models.CharField(max_length=100, blank=True, null=True)  # Field name made lowercase.
    meaning = models.CharField(max_length=2555, blank=True, null=True)

    def __str__(self):
        return self.word

    class Meta:
        db_table = 'finnish'
        app_label = 'teaching_material'
