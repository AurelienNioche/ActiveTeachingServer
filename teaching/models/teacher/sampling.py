from django.db import models

import numpy as np
import itertools as it

from user.models.user import User


class Sampling(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()
    learnt_threshold = models.FloatField()

    n_sample = models.IntegerField()

    time_per_iter = models.IntegerField()

    class Meta:

        db_table = 'sampling'
        app_label = 'teaching'

    def _revise_goal(self, now, session):

        next_ss_available = session.next_available_time.timestamp()
        ss_n_iter = session.n_iteration
        ss_it = session.iter

        h = ss_n_iter - ss_it
        ts = now + np.arange(h) * self.time_per_iter
        eval_ts = next_ss_available
        return h, ts, eval_ts

    def _select_item(self, learner, param, now, session):

        horizon, ts, eval_ts = self._revise_goal(now, session)

        new_ts = np.hstack((learner.ts, ts))

        if learner.n_seen < self.n_item:
            items = np.hstack((learner.seen_item,
                               [learner.n_seen, ]))
        else:
            items = np.arange(self.n_item)

        n_perm = self.n_item ** horizon

        if n_perm < self.n_sample:

            r1 = np.zeros(n_perm)
            r2 = np.zeros(n_perm)
            first = np.zeros(n_perm, dtype=int)
            for i, future in enumerate(it.product(items, repeat=horizon)):
                first[i] = future[0]
                r1[i], r2[i] = self._value_future(
                    future=future, param=param,
                    new_ts=new_ts, eval_ts=eval_ts,
                    learner=learner)

        else:

            r1 = np.zeros(self.n_sample)
            r2 = np.zeros(self.n_sample)
            first = np.zeros(self.n_sample, dtype=int)
            for i in range(self.n_sample):
                future = np.random.choice(items, replace=True, size=horizon)
                first[i] = future[0]
                r1[i], r2[i] = self._value_future(
                    future=future, param=param,
                    new_ts=new_ts, eval_ts=eval_ts,
                    learner=learner)

        if np.all(r1 == r1[0]):
            r = r1
        else:
            r = r2

        item_idx = first[np.argmax(r)]

        return item_idx

    def _value_future(self, learner, future, param, new_ts, eval_ts):

        new_hist = np.hstack((learner.hist, future))

        p_seen, seen = learner.p_seen_spec_hist(
            param=param, hist=new_hist,
            ts=new_ts,
            now=eval_ts
        )
        return np.sum(p_seen > self.learnt_threshold), np.sum(p_seen)

    def ask(self, learner, param, now, session):

        item_idx = self._select_item(learner=learner, param=param, now=now,
                                     session=session)
        return item_idx


# horizon = models.IntegerField()

# So need to set them at creation ---
# plan_it = models.IntegerField(default=0)

# def _revise_goal(self, now, session):
    #
    #     next_ss_available = session.next_available_time.timestamp()
    #     ss_n_iter = session.n_iteration
    #     ss_it = session.iter
    #
    #     assert self.horizon <= ss_n_iter, "Case not handled!"
    #
    #     remain = ss_n_iter - ss_it
    #
    #     self.plan_it += 1
    #     if self.plan_it == self.horizon:
    #         self.plan_it = 0
    #         h = self.horizon
    #     else:
    #         h = self.horizon - self.plan_it
    #
    #     timestamps = now + np.arange(h + 1, dtype=int) * self.time_per_iter
    #
    #     if remain < h + 1:
    #         pred_no_break_time = now + remain * self.time_per_iter
    #         delay = max(0, next_ss_available - pred_no_break_time)
    #
    #         timestamps[remain:] += delay
    #
    #     return h, timestamps

