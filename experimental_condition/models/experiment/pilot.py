from django.db import models

from user.models.user import User


class PilotManager(models.Manager):

    def create(self):

        obj = super().create()
        return obj




class Pilot(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = PilotManager()