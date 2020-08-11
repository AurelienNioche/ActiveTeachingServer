from django.db import models
from django.contrib.postgres.fields import ArrayField

from user.models.user import User

import numpy as np


class EvaluatorManager(models.Manager):

    def create(self, user, n_item, n_repetition):

        seen = list(np.zeros(n_item))

        obj = super().create(
            user=user,
            seen=seen,
            n_item=n_item,
            n_repetition=n_repetition
        )
        return obj


class Evaluator(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()

    seen = ArrayField(models.BooleanField(), default=list)

    n_repetition = models.IntegerField()

    # Set afterwards ---
    evaluation_schedule = ArrayField(models.IntegerField(), default=list)
    iter = models.IntegerField(default=0)

    eval_done = models.BooleanField(default=False)

    objects = EvaluatorManager()

    class Meta:

        db_table = 'evaluator'
        app_label = 'teaching'

    def ask(self):
        if self.iter == 0:
            self.make_evaluation_schedule()
        item = self.evaluation_schedule[self.iter]
        self.iter += 1
        if self.iter == self.n_eval:
            self.eval_done = True
        self.save()
        return item

    @property
    def n_eval(self):
        return np.sum(self.seen) * self.n_repetition

    def make_evaluation_schedule(self):

        items_to_eval = np.flatnonzero(self.seen)
        n_seen = np.sum(self.seen)
        self.evaluation_schedule = list(np.hstack(
            [np.random.choice(items_to_eval, replace=False, size=n_seen)]))
        self.save()

    def update(self, idx_last_q):
        self.seen[idx_last_q] = True
        self.save()
