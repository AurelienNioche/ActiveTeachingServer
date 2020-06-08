from django.db import models
from django.utils import timezone
import datetime

from . user import User


class SessionManager(models.Manager):

    def create(self, user):
        # Do some extra stuff here on the submitted data before saving...

        last_session = \
            user.session_set.order_by("available_time").reverse().first()

        if last_session is None:
            available_time = timezone.now()
            print(f"No previous session existing for {user.email}, I'm creating a new one now, available now ({available_time} UTC)")
        else:

            available_time = \
                last_session.available_time + datetime.timedelta(minutes=5)

            print(
                f"Previous session was available at {last_session.available_time} UTC for user {user.email}, \n"
                f"I'm creating a new one now, available 5 min later than the previous one ({available_time} UTC)")

            print("now", timezone.now())
            print("next available time", available_time)

        if user.condition == user.Condition.TEST:
            # n_completed_session = self.session_set.count()
            obj = super().create(
                user=user,
                available_time=available_time,
                n_iteration=3
            )

            return obj

        else:
            raise ValueError


class Session(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    available_time = models.DateTimeField(null=True, blank=True)
    n_iteration = models.IntegerField(default=100)
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
        print("now", timezone.now())
        print("available time", self.available_time)
        return self.available_time <= timezone.now()

    @classmethod
    def get_user_session(cls, user):

        session = user.session_set.filter(close=False).first()
        if session is None:
            session = cls.objects.create(user=user)

        return session
