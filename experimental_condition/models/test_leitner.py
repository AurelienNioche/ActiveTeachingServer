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
               n_iter_ss=15, n_ss=2):

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
                             n_iter_ss=n_iter_ss, n_ss=n_ss)
        return obj


class TestLeitner(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    teaching_engine = models.OneToOneField(TeachingEngine,
                                           on_delete=models.CASCADE)

    n_iter_ss = models.IntegerField()
    n_ss = models.IntegerField()

    objects = TestLeitnerManager()

    class Meta:

        db_table = 'test_leitner'
        app_label = 'experimental_condition'

    def new_session(self):
        from user.models.session import Session

        if self.teaching_engine.evaluator.eval_done:
            return None

        is_evaluation = self.teaching_engine.session_set.count() == self.n_ss

        if is_evaluation:
            n_iteration = self.teaching_engine.evaluator.get_n_eval()
        else:
            n_iteration = self.n_iter_ss

        obj = Session.objects.create(
            user=self.user,
            available_time=timezone.now(),
            next_available_time=None,
            n_iteration=n_iteration,
            teaching_engine=self.teaching_engine,
            is_evaluation=is_evaluation)

        return obj
