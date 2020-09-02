from django.db import models
# from django.contrib.postgres.fields import ArrayField

import numpy as np

from user.models.user import User


class Recursive(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()
    learnt_threshold = models.FloatField()

    n_iter_per_session = models.IntegerField()
    time_per_iter = models.IntegerField()

    class Meta:

        db_table = 'recursive'
        app_label = 'teaching'

    def _recursive_exp_decay(self,
                             n_pres, last_pres,
                             future_ts, param, eval_ts,
                             cst_time, is_item_specific):

        itr = 0
        n_item = self.n_item

        thr = self.learnt_threshold

        first_item = None

        n_pres_current = np.array(n_pres, dtype=int)
        last_pres_current = np.array(last_pres, dtype=float)
        print("future ts", future_ts)

        while True:

            n_pres = n_pres_current[:n_item].copy()
            last_pres = last_pres_current[:n_item].copy()

            print("n item", n_item)

            for i, ts in enumerate(future_ts):

                if np.max(n_pres) == 0:
                    item = 0
                else:
                    seen = n_pres > 0

                    if is_item_specific:
                        init_forget = param[:n_item][seen, 0]
                        rep_effect = param[:n_item][seen, 1]
                    else:
                        init_forget, rep_effect = param

                    p_seen = np.exp(
                        -init_forget
                        * (1 - rep_effect) ** (n_pres[seen] - 1)
                        * (ts - last_pres[seen])
                        * cst_time)

                    if np.min(p_seen) <= 0.90 or np.sum(seen) == n_item:
                        item = np.flatnonzero(seen)[np.argmin(p_seen)]
                    else:
                        item = np.max(np.flatnonzero(seen)) + 1

                if i == 0:
                    first_item = item

                n_pres[item] += 1
                last_pres[item] = ts

            seen = n_pres > 0

            if is_item_specific:
                init_forget = param[:n_item][seen, 0]
                rep_effect = param[:n_item][seen, 1]
            else:
                init_forget, rep_effect = param

            p_seen = np.exp(
                -init_forget
                * (1 - rep_effect) ** (n_pres[seen] - 1)
                * (eval_ts - last_pres[seen])
                * cst_time)

            n_learnt = np.sum(p_seen > thr)

            if n_learnt == n_item:
                break
            else:
                print("n pres", n_pres)
                n_item = np.sum(n_pres > 0) - 1
                print("new n item", n_item)

                if n_item < 1:
                    break
                else:
                    itr += 1
                    continue

        return first_item

    def _get_future_ts(self, now, session, next_sessions, eval_time):

        next_ss_ts = sorted([ts.available_time.timestamp()
                             for ts in next_sessions])
        eval_ts = eval_time.timestamp()
        ss_iter = session.get_iter()

        r = self.n_iter_per_session - ss_iter
        this_ss_ts = now + np.arange(r) * self.time_per_iter

        other_ts = [nts
                    + np.arange(self.n_iter_per_session) * self.time_per_iter
                    for nts in next_ss_ts]

        ts = np.hstack((this_ss_ts, *other_ts))

        return ts, eval_ts

    def ask(self, learner, param, now, session, next_sessions, eval_time):

        ts, eval_ts = self._get_future_ts(
            now=now, session=session,
            next_sessions=next_sessions,
            eval_time=eval_time)

        n_pres, last_pres = learner.n_pres, learner.last_pres
        cst_time = learner.cst_time

        is_item_specific = len(param.shape) > 1

        item_idx = self._recursive_exp_decay(
            param=param,
            future_ts=ts,
            eval_ts=eval_ts,
            cst_time=cst_time,
            is_item_specific=is_item_specific,
            n_pres=n_pres,
            last_pres=last_pres)

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

