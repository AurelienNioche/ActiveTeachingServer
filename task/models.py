from django.utils.timezone import now

from django.db import models

# Create your models here.


class Question(models.Model):

    user_id = models.IntegerField(default=-1)
    t = models.IntegerField(default=-1)
    question = models.IntegerField(default=-1)
    possible_reply_0 = models.IntegerField(default=-1)
    possible_reply_1 = models.IntegerField(default=-1)
    possible_reply_2 = models.IntegerField(default=-1)
    possible_reply_3 = models.IntegerField(default=-1)
    possible_reply_4 = models.IntegerField(default=-1)
    possible_reply_5 = models.IntegerField(default=-1)
    reply = models.IntegerField(default=-1)
    success = models.BooleanField()
    time_display = models.DateTimeField(default=now)
    time_reply = models.DateTimeField(default=now)

    class Meta:

        db_table = 'question'
        app_label = 'task'


class User(models.Model):

    # username = models.TextField(unique=True)
    # gender = models.TextField(blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)
    # mother_tongue = models.TextField(blank=True, null=True)
    # other_language = models.TextField(blank=True, null=True)
    # t = models.IntegerField(blank=True, null=True, default=0)
    teacher = models.CharField(max_length=255,
                               blank=True, null=True,
                               default='<empty>')
    registration_time = models.DateTimeField(default=now)

    class Meta:
        db_table = 'user'
        app_label = 'task'

# class PredefinedQuestion(models.Model):
#
#     t = models.IntegerField(default=-1)
#     question = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     correct_answer = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     possible_reply_0 = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     possible_reply_1 = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     possible_reply_2 = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     possible_reply_3 = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     possible_reply_4 = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#     possible_reply_5 = models.CharField(max_length=255, blank=True, null=True, default='<empty>')
#
#     class Meta:
#         db_table = 'predefined_question'
#         app_label = 'task'