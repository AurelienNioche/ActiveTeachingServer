from django.db import models
from django.utils import timezone

import datetime
import numpy as np

from user.models.user import User

from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.sampling import Sampling
from teaching.models.psychologist.bayesian_grid import Psychologist

from teaching.models.learner.exp_decay import ExpDecay
from teaching.models.learner.walsh import Walsh2018


class PilotManager(models.Manager):

    def create(self, user, material, leitner_delay_factor,
               leitner_delay_min, eval_n_repetition,
               n_iter_ss, n_ss,
               learnt_threshold, sampling_iter_limit,
               sampling_horizon, time_per_iter,
               exp_decay_grid_size, exp_decay_bounds,
               is_item_specific=False):

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

        sampling = Sampling.objects.create(
            user=user,
            n_item=n_item,
            learnt_threshold=learnt_threshold,
            iter_limit=sampling_iter_limit,
            horizon=sampling_horizon,
            time_per_iter=time_per_iter)

        psy = Psychologist.objects.create(
            user=user,
            n_item=n_item,
            is_item_specific=is_item_specific,
            grid_size=exp_decay_grid_size,
            bounds=exp_decay_bounds)

        exp_decay = ExpDecay.objects.create(
            n_item=n_item,
            user=user)

        ev = Evaluator.objects.create(
            user=user,
            n_item=n_item,
            n_repetition=eval_n_repetition
        )

        exp_decay_te = TeachingEngine.objects.create(
            user=user,
            material=material,
            sampling=sampling,
            psychologist=psy,
            exp_decay=exp_decay,
            evaluator=ev
        )

        obj = super().create(
            user=user,
            leitner_teaching_engine=leitner_te,
            active_teaching_engine=exp_decay_te,
            n_iter_ss=n_iter_ss,
            n_ss=n_ss
        )
        return obj


class Pilot(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    leitner_teaching_engine = models.OneToOneField(TeachingEngine,
                                                   on_delete=models.CASCADE)

    active_teaching_engine = models.OneToOneField(TeachingEngine,
                                                  on_delete=models.CASCADE)

    n_iter_ss = models.IntegerField()
    n_ss = models.IntegerField()

    first_session = models.TimeField()
    second_session = models.TimeField()

    n_ss_open_today = models.IntegerField()

    objects = PilotManager()

    def new_session(self):
        from user.models.session import Session

        user_sessions = \
            self.user.session_set.order_by("available_time").reverse()

        last_session = user_sessions.first()
        if last_session is None:
            te = self.active_teaching_engine if np.random.choice([0, 1]) \
                else self.leitner_teaching_engine

            available_time = timezone.now().replace(
                hour=self.first_session.hour,
                minute=self.first_session.minute)
            if available_time < timezone.now():
                available_time += datetime.timedelta(days=1)

        elif last_session.available_time.time() == self.first_session:

            # First session => use same teacher as last session
            te = last_session.teaching_engine
            available_time = timezone.now().replace(
                hour=self.first_session.hour,
                minute=self.first_session.minute)
            if last_session.available_time.date() == timezone.now().date():
                available_time += datetime.timedelta(days=1)

            next_available_time = available_time.replace(
                hour=self.second_session.hour,
                minute=self.second_session.minute
            )
            next_available_time += datetime.timedelta(days=1)

        else:
            # Second session => change teacher
            if last_session.teaching_engine == self.leitner_teaching_engine:
                te = self.active_teaching_engine
            else:
                te = self.leitner_teaching_engine

            available_time = last_session.available_time.replace(
                hour=self.second_session.hour,
                minute=self.second_session.minute)
            next_available_time = available_time.replace(
                hour=self.first_session.hour,
                minute=self.first_session.minute
            )
            next_available_time += datetime.timedelta(days=1)

        is_evaluation = te.session_set.count() == self.n_ss

        if is_evaluation:
            if te.evaluator.eval_done:
                return None
            else:
                n_iteration = te.evaluator.n_eval
                next_available_time = None
        else:
            n_iteration = self.n_iter_ss
            next_available_time = None

        obj = Session.objects.create(
            user=self.user,
            available_time=available_time,
            next_available_time=next_available_time,
            # + datetime.timedelta(minutes=0),
            n_iteration=n_iteration,
            teaching_engine=te)

        return obj
