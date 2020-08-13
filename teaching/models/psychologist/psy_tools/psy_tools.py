from django.db import models
from django.contrib.postgres.fields import ArrayField

from user.models.user import User


class Param(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.IntegerField()

    value = ArrayField(models.FloatField(), default=list)


class LogPost(Param):

    pass
