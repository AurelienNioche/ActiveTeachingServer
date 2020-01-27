from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.utils.timezone import now

from learner.models.user import User
from teaching_material.models import Kanji
from teaching_material.models import Meaning


class QuestionManager(models.Manager):

    def create(self, possible_replies, **kwargs):
        # Do some extra stuff here on the submitted data before saving...

        # Now call the super method which does the actual creation
        obj = super().create(**kwargs)
        for pr in possible_replies:
            obj.possible_replies.add(pr)

        return obj


class Question(models.Model):

    # Set at the moment of the creation
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t = models.IntegerField(default=-1)
    question = models.ForeignKey(Kanji, on_delete=models.SET_NULL,
                                 null=True)

    possible_replies = models.ManyToManyField(Meaning,
                                              related_name="possible_replies")
    new = models.BooleanField()

    # Set after the user reply
    user_reply = models.ForeignKey(Meaning, on_delete=models.SET_NULL,
                                   null=True, default=None,
                                   related_name='user_reply')
    success = models.BooleanField(null=True, default=None)
    time_display = models.DateTimeField(default=now)
    time_reply = models.DateTimeField(default=now)

    objects = QuestionManager()

    class Meta:

        db_table = 'question'
        app_label = 'learner'
