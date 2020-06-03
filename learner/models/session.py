from django.db import models
from django.utils import timezone

from teacher.models import Leitner
from . user import User


class Session(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    available_time = models.TimeField(auto_now_add=True)
    leitner_teacher = models.ForeignKey(Leitner, blank=True, null=True)
    n_iteration = models.IntegerField(default=100)
    close = models.BooleanField(default=False)

    class Meta:
        db_table = 'session'
        app_label = 'learner'

    @property
    def done(self):
        n_question = self.question_set.exclude(user_reply=None).count()
        if n_question == self.n_iteration:
            return True
        else:
            return False

    @property
    def iter(self):
        n_question = self.question_set.exclude(user_reply=None).count()
        return n_question

    def is_available(self):

        return self.available_time <= timezone.now()

