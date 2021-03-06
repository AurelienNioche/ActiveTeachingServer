from django.db import models

from user.models.user import User

import numpy as np


class Threshold(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()
    learnt_threshold = models.FloatField()

    class Meta:

        db_table = 'threshold'
        app_label = 'teaching'

    def _select_item(self, learner, param, now):

        p, seen = learner.p_seen(param=param, now=now)
        min_p = np.min(p)

        if np.sum(seen) == self.n_item or min_p <= self.learnt_threshold:
            item_idx = np.flatnonzero(seen)[np.argmin(p)]

        else:
            item_idx = np.argmin(seen)

        return item_idx

    def ask(self, learner, param, now):
        return self._select_item(learner=learner, param=param, now=now)
