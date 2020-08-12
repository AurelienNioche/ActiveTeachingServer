from django.db import models
from django.utils import timezone

from teaching.models.teaching_engine import TeachingEngine
from user.models.user import User


from experimental_condition import experimental_condition


class Session(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_creation = models.DateTimeField(auto_now_add=True)
    available_time = models.DateTimeField()
    next_available_time = models.DateTimeField(null=True)
    n_iteration = models.IntegerField()
    open = models.BooleanField(default=True)

    is_evaluation = models.BooleanField(default=False)

    teaching_engine = models.ForeignKey(TeachingEngine,
                                        on_delete=models.CASCADE)

    class Meta:
        db_table = 'session'
        app_label = 'user'

    @property
    def done(self):
        n_question = self.question_set.exclude(user_reply=None).count()
        if n_question == self.n_iteration:
            self.open = False
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

        session = user.session_set.filter(open=True).first()
        if session is None:
            session = experimental_condition.session_creation(user=user)

        return session
