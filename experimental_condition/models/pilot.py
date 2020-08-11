from django.db import models

from user.models.user import User

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine


class PilotManager(models.Manager):

    def create(self, user, material, leitner_delay_factor,
               leitner_delay_min, eval_n_repetition,
               n_iter_ss):

        n_item = material.count()

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

        leitner_te = TeachingEngine.objects.create(
            user=user,
            material=material,
            leitner=leitner,
            evaluator=ev
        )

        is_item_specific = False
        #
        #     sampling = Sampling.objects.create(
        #         user=user,
        #         n_item=n_item,
        #         learnt_threshold=learnt_threshold,
        #         iter_limit=sampling_iter_limit,
        #         horizon=sampling_horizon,
        #         time_per_iter=time_per_iter)
        #
        #     psy = Psychologist.objects.create(
        #         user=user,
        #         n_item=n_item,
        #         is_item_specific=is_item_specific,
        #         grid_size=exp_decay_grid_size,
        #         bounds=exp_decay_bounds)
        #
        #     exp_decay = ExpDecay.objects.create(
        #         n_item=n_item,
        #         user=user)
        #
        #     ev = Evaluator.objects.create(
        #         user=user,
        #         n_item=n_item,
        #         n_repetition=eval_n_repetition
        #     )
        #
        #     TeachingEngine.objects.create(
        #         user=user,
        #         material=material,
        #         sampling=sampling,
        #         psychologist=psy,
        #         exp_decay=exp_decay,
        #         evaluator=ev
        #     )

        obj = super().create(
            user=user,
            leitner_teaching_engine=leitner_te,
            n_iter_ss=n_iter_ss
        )
        return obj


class Pilot(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    leitner_teaching_engine = models.ForeignKey(TeachingEngine,
                                                on_delete=models.CASCADE)

    n_iter_ss = models.IntegerField()

    objects = PilotManager()