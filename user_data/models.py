from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.utils.timezone import now
# import numpy as np


class Question(models.Model):

    user_id = models.IntegerField(default=-1)
    t = models.IntegerField(default=-1)
    question = models.IntegerField(default=-1)
    possible_replies = ArrayField(models.IntegerField(), default=list)
    reply = models.IntegerField(default=-1)
    success = models.BooleanField()
    time_display = models.DateTimeField(default=now)
    time_reply = models.DateTimeField(default=now)

    class Meta:

        db_table = 'question'
        app_label = 'user_data'


class User(models.Model):

    # username = models.TextField(unique=True)
    # gender = models.TextField(blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)
    # mother_tongue = models.TextField(blank=True, null=True)
    # other_language = models.TextField(blank=True, null=True)
    # t = models.IntegerField(blank=True, null=True, default=0)
    # teacher = models.CharField(max_length=255,
    #                            blank=True, null=True,
    #                            default='<empty>')
    registration_time = models.DateTimeField(default=now)

    class Meta:
        db_table = 'user'
        app_label = 'user_data'
