from django.db import models
from django.utils import timezone

import datetime
import numpy as np

from user.models.user import User

from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.sampling import Sampling
from teaching.models.psychologist.bayesian_grid import Psychologist

from teaching_material.models.kanji import Kanji

from teaching.models.learner.exp_decay import ExpDecay
from teaching.models.learner.walsh import Walsh2018


class TestActiveManager(models.Manager):

    def create(self, user,
               psychologist_model="Psychologist",
               teacher_model="Sampling",
               learner_model="Walsh2018",
               exp_decay_grid_size=20,
               exp_decay_bounds=((0.001, 0.2), (0.00, 0.5)),
               exp_cst_time=1 / (24 * 60**2),
               walsh_grid_size=10,
               walsh_bounds=(
                       (0.5, 1.5),
                       (0.001, 0.10),
                       (0.001, 0.20),
                       (0.001, 0.20),
                       (0.1, 0.1),
                       (0.6, 0.6)),
               walsh_cst_time=1 / (24 * 60**2),
               eval_n_repetition=2,
               n_item=50,
               n_iter_ss=100,
               n_ss=1,
               learnt_threshold=0.90,
               sampling_n_sample=500,
               time_per_iter=2,
               is_item_specific=True):

        material = list(Kanji.objects.all())
        selection = np.random.choice(
            material, size=n_item,
            replace=False)

        active_teaching_material = selection[:n_item]

        if teacher_model == Sampling.__name__:

            sampling = Sampling.objects.create(
                user=user,
                n_item=n_item,
                learnt_threshold=learnt_threshold,
                n_sample=sampling_n_sample,
                time_per_iter=time_per_iter)
            teacher_kwarg = {"sampling": sampling}

        elif teacher_model == Threshold.__name__:

            threshold = Threshold.objects.create(
                    user=user,
                    n_item=n_item,
                    learnt_threshold=learnt_threshold)
            teacher_kwarg = {"threshold": threshold}

        else:
            raise ValueError("Model not recognized")

        if learner_model == ExpDecay.__name__:
            exp_decay = ExpDecay.objects.create(
                n_item=n_item,
                user=user,
                cst_time=exp_cst_time)
            learner_kwarg = {"exp_decay": exp_decay}
            grid_kwarg = {"grid_size": exp_decay_grid_size,
                          "bounds": exp_decay_bounds}

        elif learner_model == Walsh2018.__name__:
            walsh = Walsh2018.objects.create(
                n_item=n_item,
                user=user,
                cst_time=walsh_cst_time)
            learner_kwarg = {"walsh": walsh}
            grid_kwarg = {"grid_size": walsh_grid_size,
                          "bounds": walsh_bounds}
        else:
            raise ValueError("Model not recognized")

        if psychologist_model == Psychologist.__name__:
            psy = Psychologist.objects.create(
                user=user,
                n_item=n_item,
                is_item_specific=is_item_specific,
                **grid_kwarg)
            psy_kwarg = {"psychologist": psy}
        else:
            raise ValueError("Model not recognized")

        ev = Evaluator.objects.create(
            user=user,
            n_item=n_item,
            n_repetition=eval_n_repetition
        )

        active_teaching_te = TeachingEngine.objects.create(
            user=user,
            material=active_teaching_material,
            evaluator=ev,
            **psy_kwarg, **learner_kwarg, **teacher_kwarg
        )

        obj = super().create(
            user=user,
            teaching_engine=active_teaching_te,
            n_iter_ss=n_iter_ss,
            n_ss=n_ss)
        return obj


class TestActive(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    teaching_engine = models.OneToOneField(
        TeachingEngine,
        on_delete=models.CASCADE)

    n_iter_ss = models.IntegerField()
    n_ss = models.IntegerField()

    objects = TestActiveManager()

    class Meta:

        db_table = 'test_active'
        app_label = 'experimental_condition'

    def new_session(self):
        from user.models.session import Session

        if self.teaching_engine.evaluator.eval_done:
            return None

        available_time = timezone.now()
        next_available_time = timezone.now() + datetime.timedelta(days=1)

        is_evaluation = self.teaching_engine.session_set.count() == self.n_ss

        if is_evaluation:
            n_iteration = self.teaching_engine.evaluator.get_n_eval()
            next_available_time = None
        else:
            n_iteration = self.n_iter_ss

        obj = Session.objects.create(
            user=self.user,
            available_time=available_time,
            next_available_time=next_available_time,
            n_iteration=n_iteration,
            teaching_engine=self.teaching_engine,
            is_evaluation=is_evaluation)

        return obj
