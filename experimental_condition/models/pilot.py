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

from teaching_material.models.kanji import Kanji

from teaching.models.learner.exp_decay import ExpDecay
from teaching.models.learner.walsh import Walsh2018


class PilotManager(models.Manager):

    def create(self, user,
               psychologist_model="Psychologist",
               teacher_model="Sampling",
               learner_model="Walsh2018",
               exp_decay_grid_size=20,
               exp_decay_bounds=((0.001, 0.04), (0.2, 0.5)),
               walsh_grid_size=10,
               walsh_bounds=(
                (0.5, 1.5),
                (0.005, 0.10),
                (0.005, 0.20),
                (0.005, 0.20),
                (0.1, 0.1),
                (0.6, 0.6)),
               leitner_delay_factor=2,
               leitner_delay_min=2,
               eval_n_repetition=2,
               n_item=100,
               n_iter_ss=100,
               n_ss=6,
               learnt_threshold=0.90,
               sampling_iter_limit=500,
               sampling_horizon=100,
               time_per_iter=2,
               first_session=datetime.time(hour=7, minute=0, second=0,
                                           microsecond=0),
               second_session=datetime.time(hour=7, minute=5, second=0,
                                            microsecond=0),
               is_item_specific=True):

        material = list(Kanji.objects.all())
        selection = np.random.choice(
            material, size=n_item*2,
            replace=False)

        leitner_material = selection[:n_item]
        active_teaching_material = selection[n_item:]

        leitner = Leitner.objects.create(
            user=user,
            n_item=n_item,
            delay_factor=leitner_delay_factor,
            delay_min=leitner_delay_min)

        ev = Evaluator.objects.create(
            user=user,
            n_item=n_item,
            n_repetition=eval_n_repetition)

        leitner_te = TeachingEngine.objects.create(
            user=user,
            material=leitner_material,
            leitner=leitner,
            evaluator=ev)

        if teacher_model == Sampling.__name__:

            sampling = Sampling.objects.create(
                user=user,
                n_item=n_item,
                learnt_threshold=learnt_threshold,
                iter_limit=sampling_iter_limit,
                horizon=sampling_horizon,
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
                user=user)
            learner_kwarg = {"exp_decay": exp_decay}
            grid_kwarg = {"grid_size": exp_decay_grid_size,
                          "bounds": exp_decay_bounds}
        elif learner_model == Walsh2018.__name__:
            walsh = Walsh2018.objects.create(
                n_item=n_item,
                user=user)
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
            n_repetition=eval_n_repetition)

        active_teaching_te = TeachingEngine.objects.create(
            user=user,
            material=active_teaching_material,
            evaluator=ev,
            **psy_kwarg, **learner_kwarg, **teacher_kwarg)

        obj = super().create(
            user=user,
            leitner_teaching_engine=leitner_te,
            active_teaching_engine=active_teaching_te,
            n_iter_ss=n_iter_ss,
            n_ss=n_ss,
            first_session=first_session,
            second_session=second_session)
        return obj


class Pilot(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    leitner_teaching_engine = models.OneToOneField(
        TeachingEngine,
        on_delete=models.CASCADE,
        related_name="leitner_teaching_engine")

    active_teaching_engine = models.OneToOneField(
        TeachingEngine,
        on_delete=models.CASCADE,
        related_name="active_teaching_engine")

    n_iter_ss = models.IntegerField()
    n_ss = models.IntegerField()

    first_session = models.TimeField()
    second_session = models.TimeField()

    objects = PilotManager()

    class Meta:

        db_table = 'pilot'
        app_label = 'experimental_condition'

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
                minute=self.first_session.minute,
                microsecond=self.first_session.microsecond)
            if available_time < timezone.now():
                available_time += datetime.timedelta(days=1)

            next_available_time = available_time.replace(
                hour=self.second_session.hour,
                minute=self.second_session.minute,
                microsecond=self.second_session.microsecond
            ) + datetime.timedelta(days=1)

        elif last_session.available_time.time() == self.second_session:

            # First session => use same teacher as last session
            te = last_session.teaching_engine
            available_time = last_session.available_time.replace(
                hour=self.first_session.hour,
                minute=self.first_session.minute,
                microsecond=self.first_session.microsecond) \
                + datetime.timedelta(days=1)

            next_available_time = available_time.replace(
                hour=self.second_session.hour,
                minute=self.second_session.minute,
                microsecond=self.second_session.microsecond) \
                + datetime.timedelta(days=1)

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
            ) + datetime.timedelta(days=1)

        if te.evaluator.eval_done:
            return None
        else:
            is_evaluation = te.session_set.count() == self.n_ss

            if is_evaluation:
                if te.evaluator.eval_done:
                    return None
                else:
                    n_iteration = te.evaluator.n_eval
                    next_available_time = None
            else:
                n_iteration = self.n_iter_ss

            obj = Session.objects.create(
                user=self.user,
                available_time=available_time,
                next_available_time=next_available_time,
                n_iteration=n_iteration,
                teaching_engine=te,
                is_evaluation=is_evaluation)

            return obj
