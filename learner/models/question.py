from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.utils.timezone import now


from . user import User
from teaching_material.models import Kanji
from teaching_material.models import Meaning


class Question(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t = models.IntegerField(default=-1)
    question = models.ForeignKey(Kanji, on_delete=models.SET_NULL,
                                 null=True)
    correct_reply = models.ForeignKey(Meaning, on_delete=models.SET_NULL,
                                      null=True,
                                      related_name='correct_reply')
    user_reply = models.ForeignKey(Meaning, on_delete=models.SET_NULL,
                                   null=True, default=None,
                                   related_name='user_reply')
    possible_replies = models.ManyToManyField(Meaning,
                                              related_name="possible_replies")
    success = models.BooleanField()
    time_display = models.DateTimeField(default=now)
    time_reply = models.DateTimeField(default=now)

    class Meta:

        db_table = 'question'
        app_label = 'learner'
