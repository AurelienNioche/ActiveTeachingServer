from django.db import models
from django.utils import timezone
import datetime

from learner.models.user import User
from teacher.models.leitner import Leitner
from teacher.models.threshold import Threshold


class SessionManager(models.Manager):

    def create(self, user):

        last_session = \
            user.session_set.order_by("available_time").reverse().first()

        if last_session is None:
            available_time = timezone.now()
        else:

            available_time = \
                last_session.available_time + datetime.timedelta(minutes=5)

        if user.condition == User.Condition.TEST:

            obj = super().create(
                user=user,
                available_time=available_time,
                n_iteration=3,
                leitner=user.leitner,
                threshold=None,
            )

            return obj

        else:
            raise ValueError


class Session(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leitner = models.ForeignKey(Leitner, on_delete=models.CASCADE, null=True)
    threshold = models.ForeignKey(Threshold, on_delete=models.CASCADE, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    available_time = models.DateTimeField()
    n_iteration = models.IntegerField()
    close = models.BooleanField(default=False)

    objects = SessionManager()

    class Meta:
        db_table = 'session'
        app_label = 'learner'

    @property
    def done(self):
        n_question = self.question_set.exclude(user_reply=None).count()
        if n_question == self.n_iteration:
            self.close = True
            self.save()
            return True
        else:
            return False

    @property
    def iter(self):
        n_question = self.question_set.exclude(user_reply=None).count()
        return n_question

    def is_available(self):
        return self.available_time <= timezone.now()

    @classmethod
    def get_user_session(cls, user):

        session = user.session_set.filter(close=False).first()
        if session is None:
            session = cls.objects.create(user=user)

        return session
