from django.db import models

from user.models.user import User
from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching_material.models import Kanji


class TestLeitnerManager(models.Manager):

    def create(self, user, n_item, leitner_delay_factor,
               leitner_delay_min, eval_n_repetition):

        material = Kanji.objects.all()[0:n_item]

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

        TeachingEngine.objects.create(
            user=user,
            material=material,
            leitner=leitner,
            evaluator=ev
        )

        obj = super().create(user=user)
        return obj


class TestLeitner(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = TestLeitnerManager()
