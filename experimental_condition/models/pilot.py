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
               exp_decay_bounds=((0.001, 0.2), (0.00, 0.5)),
               exp_cst_time=(1/60**2)/24,
               walsh_grid_size=10,
               walsh_bounds=(
                       (0.5, 1.5),
                       (0.001, 0.10),
                       (0.001, 0.20),
                       (0.001, 0.20),
                       (0.1, 0.1),
                       (0.6, 0.6)),
               walsh_cst_time=1/(24 * 60**2),
               leitner_delay_factor=2,
               leitner_delay_min=2,
               eval_n_repetition=2,
               n_item=100,
               n_iter_ss=100,
               n_ss=6,
               learnt_threshold=0.90,
               sampling_n_sample=500,
               time_per_iter=2,
               first_session=datetime.time(hour=7, minute=0, second=0,
                                           microsecond=0),
               second_session=datetime.time(hour=7, minute=5, second=0,
                                            microsecond=0),
               is_item_specific=True):

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

        fs, ss = self.first_session, self.second_session

        last_session = user_sessions.first()
        if last_session is None:
            te = self.active_teaching_engine if np.random.choice([0, 1]) \
                else self.leitner_teaching_engine

            available_time = self.set_time(timezone.now(), fs)

            if available_time < timezone.now():
                available_time += datetime.timedelta(days=1)

            next_available_time = self.set_time(available_time, ss) \
                + datetime.timedelta(days=1)

        elif last_session.available_time.time() == self.second_session:

            # First session => use same teacher as last session
            te = last_session.teaching_engine
            available_time = self.set_time(
                last_session.available_time, fs) \
                + datetime.timedelta(days=1)

            next_available_time = self.set_time(available_time, ss) \
                + datetime.timedelta(days=1)

        elif last_session.available_time.time() == self.first_session:
            # Second session => change teacher
            if last_session.teaching_engine == self.leitner_teaching_engine:
                te = self.active_teaching_engine
            else:
                te = self.leitner_teaching_engine

            available_time = \
                self.set_time(last_session.available_time, ss)
            next_available_time = \
                self.set_time(available_time, fs) \
                + datetime.timedelta(days=1)

        else:
            raise ValueError("Last session available time doesn't make sense!")

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

    @staticmethod
    def set_time(datetime_obj, time_obj):
        return datetime_obj.replace(
            hour=time_obj.hour,
            minute=time_obj.minute,
            second=time_obj.second,
            microsecond=time_obj.microsecond)
