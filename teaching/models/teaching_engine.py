from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from teaching_material.models import Kanji

from user.models.user import User

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.sampling import Sampling
from teaching.models.teacher.recursive import Recursive
from teaching.models.teacher.forward import Forward
from teaching.models.teacher.evaluator import Evaluator
# from teaching.models.teacher.mcts import MCTSTeacher

from teaching.models.psychologist.bayesian_grid import Psychologist

from teaching.models.learner.exp_decay import ExpDecay
from teaching.models.learner.walsh import Walsh2018


class TeachingEngineManager(models.Manager):

    def create(self, material, evaluator, *args, **kwargs):

        n_item = len(material)
        id_items = [m.id for m in material]

        obj = super().create(
            n_item=n_item,
            id_items=id_items,
            evaluator=evaluator,
            *args, **kwargs)
        obj.material.set(material)
        return obj


class TeachingEngine(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    material = models.ManyToManyField(Kanji,
                                      related_name="teaching_material")
    n_item = models.IntegerField()
    id_items = ArrayField(models.IntegerField(), default=list)

    leitner = models.OneToOneField(
        Leitner,
        on_delete=models.CASCADE, null=True)

    threshold = models.OneToOneField(
        Threshold,
        on_delete=models.CASCADE, null=True)

    sampling = models.OneToOneField(
        Sampling,
        on_delete=models.CASCADE, null=True)

    recursive = models.OneToOneField(
        Recursive,
        on_delete=models.CASCADE, null=True)

    forward = models.OneToOneField(
        Forward,
        on_delete=models.CASCADE, null=True)

    psychologist = models.OneToOneField(
        Psychologist,
        on_delete=models.CASCADE, null=True)

    exp_decay = models.OneToOneField(
        ExpDecay,
        on_delete=models.CASCADE, null=True)

    walsh = models.OneToOneField(
        Walsh2018,
        on_delete=models.CASCADE, null=True)

    evaluator = models.OneToOneField(
        Evaluator,
        on_delete=models.CASCADE, null=True)

    objects = TeachingEngineManager()

    class Meta:

        db_table = 'teaching_engine'
        app_label = 'teaching'

    def _get_teacher(self):

        if self.leitner is not None:
            return self.leitner

        elif self.threshold is not None:
            return self.threshold

        elif self.recursive is not None:
            return self.recursive

        elif self.forward is not None:
            return self.forward

        elif self.sampling is not None:
            return self.sampling

        else:
            raise Exception

    def _get_psychologist(self):
        if self.psychologist is not None:
            return self.psychologist

    def _get_learner(self):
        if self.exp_decay is not None:
            return self.exp_decay
        elif self.walsh is not None:
            return self.walsh

    def ask(self, session):

        last_q_entry = self.question_set.order_by("id").reverse().first()
        if last_q_entry is None:
            q_idx = 0

        else:
            last_was_success = last_q_entry.success
            last_time_reply = last_q_entry.time_reply.timestamp()
            idx_last_q = self.id_items.index(last_q_entry.item.id)

            self.evaluator.update(idx_last_q=idx_last_q)

            if session.is_evaluation:
                q_idx = self.evaluator.ask()
            else:
                q_idx = self.teach(idx_last_q=idx_last_q,
                                   last_time_reply=last_time_reply,
                                   last_was_success=last_was_success,
                                   session=session)

        item = self.material.get(id=self.id_items[q_idx])

        self.save()
        return item

    def teach(self, last_was_success, last_time_reply, idx_last_q,
              session):

        teacher = self._get_teacher()
        now = timezone.now()
        now_ts = now.timestamp()

        if teacher.__class__ == Leitner:
            teacher.update(
                last_was_success=last_was_success,
                last_time_reply=last_time_reply,
                idx_last_q=idx_last_q)
            question_idx = teacher.ask(now=now_ts)
        else:

            psychologist = self._get_psychologist()
            learner = self._get_learner()

            assert psychologist is not None
            assert learner is not None
            psychologist.update(
                last_was_success=last_was_success,
                last_time_reply=last_time_reply,
                idx_last_q=idx_last_q,
                learner=learner)

            learner.update(
                last_time_reply=last_time_reply,
                idx_last_q=idx_last_q)

            param = psychologist.inferred_learner_param()

            if teacher.__class__ == Threshold:
                question_idx = teacher.ask(learner=learner, param=param,
                                           now=now_ts)

            elif teacher.__class__ in (Recursive, Forward):
                assert learner.__class__ == ExpDecay
                next_sessions = self.session_set.filter(
                    open=True,
                    is_evaluation=False,
                ).exclude(id=session.id)
                eval_time = \
                    self.session_set.filter(is_evaluation=True).first()\
                        .available_time
                question_idx = teacher.ask(
                    learner=learner,
                    param=param,
                    now=now_ts,
                    session=session,
                    next_sessions=next_sessions,
                    eval_time=eval_time)

            elif teacher.__class__ == Sampling:
                question_idx = teacher.ask(
                    learner=learner, param=param,
                    now=now_ts,
                    session=session)
            else:
                raise not NotImplementedError

        return question_idx
