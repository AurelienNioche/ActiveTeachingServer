from django.db import models
from django.contrib.postgres.fields import ArrayField


class WaniKani(models.Model):

    character = models.TextField()
    meaning = ArrayField(models.TextField())
    level = models.IntegerField()
    onyomi = ArrayField(models.TextField(), null=True)
    kunyomi = ArrayField(models.TextField(), null=True)
    nanori = ArrayField(models.TextField(), null=True)
    important_reading = models.TextField()

