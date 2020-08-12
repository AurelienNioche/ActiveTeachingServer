from django.db import models
from django.utils import timezone

from user.models.user import User

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching_material.models.kanji import Kanji


class TestLeitnerManager(models.Manager):

    def create(self, user, n_item=50, leitner_delay_factor=2,
               leitner_delay_min=2, eval_n_repetition=2,
               n_iter_ss=15):

        material = Kanji.objects.all()[:n_item]

        leitner = Leitner.objects.create(
            user=user,
            n_item=n_item,
            delay_factor=leitner_delay_factor,
            delay_min=leitner_delay_min)

        ev = Evaluator.objects.create(
            user=user,
            n_item=n_item,
            n_repetition=eval_n_repetition
        )

        te = TeachingEngine.objects.create(
            user=user,
            material=material,
            leitner=leitner,
            evaluator=ev
        )

        obj = super().create(user=user,
                             teaching_engine=te,
                             n_iter_ss=n_iter_ss)
        return obj


class TestLeitner(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    teaching_engine = models.OneToOneField(TeachingEngine,
                                           on_delete=models.CASCADE)

    n_iter_ss = models.IntegerField()
    objects = TestLeitnerManager()

    class Meta:

        db_table = 'test_leitner'
        app_label = 'experimental_condition'

    def new_session(self):
        from user.models.session import Session

        obj = Session.objects.create(
            user=self.user,
            available_time=timezone.now(),
            next_available_time=timezone.now(),
            n_iteration=self.n_iter_ss,
            teaching_engine=self.teaching_engine)

        return obj
