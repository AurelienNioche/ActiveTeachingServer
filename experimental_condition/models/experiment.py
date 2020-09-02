from django.db import models
# from django.utils import timezone

import datetime
import numpy as np

from user.models.user import User

from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching.models.teacher.leitner import Leitner
# from teaching.models.teacher.threshold import Threshold
# from teaching.models.teacher.sampling import Sampling
from teaching.models.teacher.recursive import Recursive

from teaching.models.psychologist.bayesian_grid import Psychologist

from teaching_material.models.kanji import Kanji

from teaching.models.learner.exp_decay import ExpDecay
# from teaching.models.learner.walsh import Walsh2018
#
# from django.contrib.postgres.fields import ArrayField


class ExperimentManager(models.Manager):

    BOUNDS = [[0.0000001, 100.0], [0.0001, 0.99]]
    GRID_METHODS = [np.geomspace, np.linspace]
    GRID_SIZE = 20
    CST_TIME = 1

    N_SESSION = 2
    N_ITER_PER_SESSION = 4

    N_ITEM = 600

    LEARNT_THRESHOLD = 0.90

    TIME_PER_ITER = 2

    IS_ITEM_SPECIFIC = True

    EVAL_N_REPETITION = 2

    LEITNER_DELAY_FACTOR = 2
    LEITNER_DELAY_MIN = 2

    TIME_DELTA_TWO_TEACHERS = datetime.timedelta(seconds=2)#datetime.timedelta(minutes=5)
    TIME_DELTA_TWO_SESSIONS = datetime.timedelta(seconds=10) ##days=1)

    def create(self, user,
               first_session=datetime.time(hour=7, minute=0, second=0,
                                           microsecond=0),
               second_session=datetime.time(hour=7, minute=5, second=0,
                                            microsecond=0)):

        assert first_session != second_session, \
            "Scheduled times for first session and " \
            "second session have to be different"

        # u = User.objects.filter(email="carlos@test.com").first()
        # m = []
        # for te in u.teachingengine_set.all():
        #     for m_id in list(te.material.values_list('id', flat=True)):
        #         m.append(m_id)
        # material = list(Kanji.objects.exclude(id__in=m))

        material = list(Kanji.objects.all())

        selection = np.random.choice(
            material, size=self.N_ITEM*2,
            replace=False)

        leitner_material = selection[:self.N_ITEM]
        active_teaching_material = selection[self.N_ITEM:]

        leitner = Leitner.objects.create(
            user=user,
            n_item=self.N_ITEM,
            delay_factor=self.LEITNER_DELAY_FACTOR,
            delay_min=self.LEITNER_DELAY_MIN)

        ev = Evaluator.objects.create(
            user=user,
            n_item=self.N_ITEM,
            n_repetition=self.EVAL_N_REPETITION)

        leitner_te = TeachingEngine.objects.create(
            user=user,
            material=leitner_material,
            leitner=leitner,
            evaluator=ev)

        exp_decay = ExpDecay.objects.create(
            n_item=self.N_ITEM,
            user=user,
            cst_time=self.CST_TIME
        )

        psy = Psychologist.objects.create(
            user=user,
            n_item=self.N_ITEM,
            is_item_specific=self.IS_ITEM_SPECIFIC,
            grid_size=self.GRID_SIZE,
            grid_methods=self.GRID_METHODS,
            bounds=self.BOUNDS
        )

        ev = Evaluator.objects.create(
            user=user,
            n_item=self.N_ITEM,
            n_repetition=self.EVAL_N_REPETITION)

        recursive = Recursive.objects.create(
            user=user,
            n_item=self.N_ITEM,
            learnt_threshold=self.LEARNT_THRESHOLD,
            time_per_iter=self.TIME_PER_ITER,
            n_iter_per_session=self.N_ITER_PER_SESSION)

        active_teaching_te = TeachingEngine.objects.create(
            user=user,
            material=active_teaching_material,
            evaluator=ev,
            exp_decay=exp_decay,
            recursive=recursive,
            psychologist=psy)

        self.create_sessions(
            active_teaching_engine=active_teaching_te,
            leitner_teaching_engine=leitner_te,
            first_session=first_session, user=user)

        obj = super().create(user=user)
        return obj

    def create_sessions(self, active_teaching_engine,
                        leitner_teaching_engine,
                        first_session, user):

        from user.models.session import Session

        teaching_engines = [active_teaching_engine, leitner_teaching_engine]

        session_time = []

        session_is_first = []

        for ss_idx in range(self.N_SESSION+1):

            for i, te in enumerate(teaching_engines):

                if not session_time:

                    available_time = first_session
                    session_time.append(available_time)
                    session_is_first.append(True)

                else:
                    if session_is_first[-1]:
                        available_time = session_time[-1] \
                                     + self.TIME_DELTA_TWO_TEACHERS

                    else:
                        available_time = session_time[-2] \
                                     + self.TIME_DELTA_TWO_SESSIONS

                    session_time.append(available_time)
                    session_is_first.append(not session_is_first[-1])

                if ss_idx < self.N_SESSION:

                    Session.objects.create(
                        user=user,
                        available_time=available_time,
                        n_iteration=self.N_ITER_PER_SESSION,
                        teaching_engine=te,
                        is_evaluation=False)

                else:
                    Session.objects.create(
                        user=user,
                        available_time=available_time,
                        n_iteration=None,
                        teaching_engine=te,
                        is_evaluation=True)


class Experiment(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = ExperimentManager()

    class Meta:

        db_table = 'experiment'
        app_label = 'experimental_condition'

    def new_session(self):
        return None
