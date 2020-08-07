from django.db import models

import numpy as np
import itertools as it

from user.models.user import User


class Sampling(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()
    learnt_threshold = models.FloatField()

    iter_limit = models.IntegerField()
    time_limit = models.IntegerField()

    time_per_iter = models.IntegerField()
    horizon = models.IntegerField()

    ss_n_iter = models.IntegerField()
    ss_n_iter_between = models.IntegerField()

    # So need to set them at creation ---
    ss_it = models.IntegerField(default=0)

    class Meta:

        db_table = 'sampling'
        app_label = 'teaching'

    def _revise_goal(self, now):

        self.ss_it += 1
        if self.ss_it == self.ss_n_iter - 1:
            self.ss_it = 0

        remain = self.ss_n_iter - self.ss_it

        self.iter += 1
        if self.iter == self.horizon:
            self.iter = 0
            h = self.horizon
        else:
            h = self.horizon - self.iter

        # delta in timestep (number of iteration)
        delta_ts = np.arange(h + 1, dtype=int)

        if remain < h + 1:
            delta_ts[remain:] += self.ss_n_iter_between
            assert h - remain <= self.ss_n_iter, "case not handled!"

        timestamps = now + delta_ts * self.time_per_iter

        return h, timestamps

    def _select_item(self, learner, param, now):

        horizon, timestamps = self._revise_goal(now)
        # print("h", horizon, "ts", len(timestamps))

        ts = np.asarray(learner.ts)
        ts = ts[ts != -1]
        new_ts = \
            np.hstack((ts, timestamps[:-1]))
        eval_ts = timestamps[-1]

        items = np.hstack((learner.seen_item,
                           [learner.n_seen, ]))

        n_item = len(items)
        n_perm = n_item ** horizon

        if n_perm < self.iter_limit:

            r = np.zeros(n_perm)
            first = np.zeros(n_perm, dtype=int)
            for i, future in enumerate(it.product(items, repeat=horizon)):
                first[i] = future[0]
                r[i] = self._value_future(future=future, param=param,
                                          new_ts=new_ts, eval_ts=eval_ts,
                                          learner=learner)

            item_idx = first[np.argmax(r)]
        else:
            r = np.zeros(self.iter_limit)
            first = np.zeros(self.iter_limit, dtype=int)
            for i in range(self.iter_limit):
                future = np.random.choice(items, replace=True, size=horizon)
                first[i] = future[0]
                r[i] = self._value_future(future=future, param=param,
                                          new_ts=new_ts, eval_ts=eval_ts,
                                          learner=learner)

            item_idx = first[np.argmax(r)]

        return item_idx

    def _value_future(self, learner, future, param, new_ts, eval_ts):
        hist = learner.hist
        hist = hist[hist != -1]
        new_hist = np.hstack((hist, future))

        p_seen, seen = learner.p_seen_spec_hist(
            param=param, hist=new_hist,
            ts=new_ts,
            now=eval_ts
        )
        return np.sum(p_seen)

    def ask(self, learner, param, now):

        item_idx = self._select_item(learner=learner, param=param, now=now)
        return item_idx
