from django.db import models

# Create your models here.


class User(models.Model):

    username = models.TextField(db_index=True, max_length=40, unique=True)
    gender = models.TextField(max_length=6, default=None, null=True)
    age = models.IntegerField(default=-1, null=True)
    mother_tongue = models.TextField(max_length=40, default=None, null=True)
    other_language = models.TextField(max_length=40, default=None, null=True)
    registration_time = models.DateTimeField(auto_now_add=True, blank=True)


class Data(models.Model):

    user_id = models.IntegerField(db_index=True, default=-1)
    t = models.IntegerField(db_index=True, default=-1)
    question = models.IntegerField(default=-1)
    reply = models.IntegerField(default=-1)
