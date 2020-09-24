from django.db import models
# from django.utils import timezone

import datetime
import numpy as np

from user.models.user import User

from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.recursive import Recursive

from teaching.models.psychologist.bayesian_grid import Psychologist

from teaching_material.models.kanji import Kanji

from teaching.models.learner.exp_decay import ExpDecay
# from teaching.models.learner.walsh import Walsh2018

# from teaching.models.teacher.sampling import Sampling
# from django.contrib.postgres.fields import ArrayField


class Task:

    BOUNDS = [[0.025, 0.00005], [0.0001, 0.9999]]
    # BOUNDS = [[0.0000001, 0.00005], [0.0001, 0.9999]]
    # [[0.0000001, 0.1], [0.0001, 0.9999]]
    GRID_METHODS = [np.logspace, np.linspace]
    GRID_SIZE = 100
    CST_TIME = 1

    N_SESSION = 6
    N_ITER_PER_SESSION = 100

    N_ITEM = 200

    LEARNT_THRESHOLD = 0.90

    TIME_PER_ITER = 4

    EVAL_N_REPETITION = 2

    TIME_DELTA_TWO_TEACHERS = datetime.timedelta(
        seconds=TIME_PER_ITER*N_ITER_PER_SESSION)
    TIME_DELTA_TWO_SESSIONS = datetime.timedelta(
        days=1)

    LEITNER_DELAY_FACTOR = 2
    LEITNER_DELAY_MIN = TIME_PER_ITER

    @classmethod
    def create_sessions(cls, active_teaching_engine,
                        leitner_teaching_engine,
                        first_session, user,
                        begin_with_active):

        from user.models.session import Session

        teaching_engines = [active_teaching_engine, leitner_teaching_engine]
        if not begin_with_active:
            teaching_engines.reverse()

        session_time = []

        session_is_first = []

        for ss_idx in range(cls.N_SESSION+1):

            for i, te in enumerate(teaching_engines):

                if not session_time:

                    available_time = first_session
                    session_time.append(available_time)
                    session_is_first.append(True)

                else:
                    if session_is_first[-1]:
                        available_time = session_time[-1] \
                                     + cls.TIME_DELTA_TWO_TEACHERS

                    else:
                        available_time = session_time[-2] \
                                     + cls.TIME_DELTA_TWO_SESSIONS

                    session_time.append(available_time)
                    session_is_first.append(not session_is_first[-1])

                if ss_idx < cls.N_SESSION:

                    Session.objects.create(
                        user=user,
                        available_time=available_time,
                        n_iteration=cls.N_ITER_PER_SESSION,
                        teaching_engine=te,
                        is_evaluation=False)

                else:
                    Session.objects.create(
                        user=user,
                        available_time=available_time,
                        n_iteration=None,
                        teaching_engine=te,
                        is_evaluation=True)

    @classmethod
    def create_leitner_engine(cls, user, material):

        leitner = Leitner.objects.create(
            user=user,
            n_item=Task.N_ITEM,
            delay_factor=cls.LEITNER_DELAY_FACTOR,
            delay_min=cls.LEITNER_DELAY_MIN)

        ev = Evaluator.objects.create(
            user=user,
            n_item=Task.N_ITEM,
            n_repetition=Task.EVAL_N_REPETITION)

        return TeachingEngine.objects.create(
            user=user,
            material=material,
            leitner=leitner,
            evaluator=ev)

    @classmethod
    def create_material(cls, previous_email=None):

        if previous_email is not None:
            u = User.objects.filter(email=previous_email).first()
            m = []
            for te in u.teachingengine_set.all():
                for m_id in list(te.material.values_list('id', flat=True)):
                    m.append(m_id)
            material = list(Kanji.objects.exclude(id__in=m))
        else:
            material = list(Kanji.objects.all())

        selection = np.random.choice(
            material, size=Task.N_ITEM * 2,
            replace=False)

        leitner_m = selection[:Task.N_ITEM]
        active_teaching_m = selection[Task.N_ITEM:]

        return leitner_m, active_teaching_m

    @classmethod
    def create_exp_decay_recursive_engine(cls, user, material,
                                          is_item_specific):

        exp_decay = ExpDecay.objects.create(
            n_item=cls.N_ITEM,
            user=user,
            cst_time=cls.CST_TIME)

        psy = Psychologist.objects.create(
            user=user,
            n_item=cls.N_ITEM,
            is_item_specific=is_item_specific,
            grid_size=cls.GRID_SIZE,
            grid_methods=cls.GRID_METHODS,
            bounds=cls.BOUNDS
        )

        ev = Evaluator.objects.create(
            user=user,
            n_item=cls.N_ITEM,
            n_repetition=cls.EVAL_N_REPETITION)

        recursive = Recursive.objects.create(
            user=user,
            n_item=cls.N_ITEM,
            learnt_threshold=cls.LEARNT_THRESHOLD,
            time_per_iter=cls.TIME_PER_ITER,
            n_iter_per_session=cls.N_ITER_PER_SESSION)

        return TeachingEngine.objects.create(
            user=user,
            material=material,
            evaluator=ev,
            exp_decay=exp_decay,
            recursive=recursive,
            psychologist=psy)

    @classmethod
    def create_exp_decay_threshold_engine(cls, user, material,
                                          is_item_specific):

        exp_decay = ExpDecay.objects.create(
            n_item=cls.N_ITEM,
            user=user,
            cst_time=cls.CST_TIME)

        psy = Psychologist.objects.create(
            user=user,
            n_item=cls.N_ITEM,
            is_item_specific=is_item_specific,
            grid_size=cls.GRID_SIZE,
            grid_methods=cls.GRID_METHODS,
            bounds=cls.BOUNDS)

        ev = Evaluator.objects.create(
            user=user,
            n_item=cls.N_ITEM,
            n_repetition=cls.EVAL_N_REPETITION)

        threshold = Threshold.objects.create(
            user=user,
            n_item=cls.N_ITEM,
            learnt_threshold=cls.LEARNT_THRESHOLD)

        return TeachingEngine.objects.create(
            user=user,
            material=material,
            evaluator=ev,
            exp_decay=exp_decay,
            threshold=threshold,
            psychologist=psy)


class RecursiveConditionManager(models.Manager):

    def create(self, user, first_session, begin_with_active,
               is_item_specific, previous_email=None):

        leitner_m, active_teaching_m = \
            Task.create_material(previous_email=previous_email)

        leitner_te = Task.create_leitner_engine(
            user=user,
            material=leitner_m)

        active_teaching_te = Task.create_exp_decay_recursive_engine(
            user=user,
            material=active_teaching_m,
            is_item_specific=is_item_specific)

        Task.create_sessions(
            active_teaching_engine=active_teaching_te,
            leitner_teaching_engine=leitner_te,
            first_session=first_session, user=user,
            begin_with_active=begin_with_active)

        obj = super().create(user=user)
        return obj


class RecursiveCondition(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = RecursiveConditionManager()

    class Meta:

        db_table = 'recursive_condition'
        app_label = 'experimental_condition'

    def new_session(self):
        return None


class ThresholdConditionManager(models.Manager):

    def create(self, user, first_session, begin_with_active,
               is_item_specific, previous_email=None):

        leitner_m, active_teaching_m = \
            Task.create_material(previous_email=previous_email)

        leitner_te = Task.create_leitner_engine(
            user=user,
            material=leitner_m)

        active_teaching_te = Task.create_exp_decay_threshold_engine(
            user=user,
            material=active_teaching_m,
            is_item_specific=is_item_specific)

        Task.create_sessions(
            active_teaching_engine=active_teaching_te,
            leitner_teaching_engine=leitner_te,
            first_session=first_session, user=user,
            begin_with_active=begin_with_active)

        obj = super().create(user=user)
        return obj


class ThresholdCondition(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = ThresholdConditionManager()

    class Meta:

        db_table = 'threshold_condition'
        app_label = 'experimental_condition'

    def new_session(self):
        return None
