from django.db import models
# from django.contrib.postgres.fields import ArrayField

import numpy as np

from user.models.user import User


class Forward(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()
    learnt_threshold = models.FloatField()

    n_iter_per_session = models.IntegerField()
    time_per_iter = models.IntegerField()

    class Meta:

        db_table = 'forward'
        app_label = 'teaching'

    def _threshold_select(self, n_pres, param, n_item, is_item_specific,
                          ts, last_pres, log_thr):

        if np.max(n_pres) == 0:
            item = 0
        else:
            seen = n_pres > 0

            log_p_seen = self._cp_log_p_seen(
                seen=seen,
                n_pres=n_pres,
                param=param,
                n_item=n_item,
                is_item_specific=is_item_specific,
                last_pres=last_pres,
                ts=ts)

            if np.min(log_p_seen) <= log_thr or np.sum(seen) == n_item:
                item = np.flatnonzero(seen)[np.argmin(log_p_seen)]
            else:
                item = np.max(np.flatnonzero(seen)) + 1

        return item

    @staticmethod
    def _cp_log_p_seen(seen, n_pres, param, n_item, is_item_specific,
                       last_pres, ts):

        if is_item_specific:
            init_forget = param[:n_item][seen, 0]
            rep_effect = param[:n_item][seen, 1]
        else:
            init_forget, rep_effect = param

        return \
            -init_forget \
            * (1 - rep_effect) ** (n_pres[seen] - 1) \
            * (ts - last_pres[seen])

    def _forward(self, n_pres, last_pres,
                 future_ts, param, eval_ts,
                 is_item_specific,
                 log_thr):

        n_item = self.n_item

        now = future_ts[0]
        future = future_ts[1:]

        n_pres_current = n_pres
        last_pres_current = last_pres

        while True:

            n_pres = n_pres_current[:n_item]
            last_pres = last_pres_current[:n_item]

            first_item = self._threshold_select(
                n_pres=n_pres,
                param=param,
                n_item=n_item,
                is_item_specific=is_item_specific,
                ts=now, last_pres=last_pres,
                log_thr=log_thr)

            n_item = first_item + 1

            n_pres = n_pres_current[:n_item].copy()
            last_pres = last_pres_current[:n_item].copy()

            n_pres[first_item] += 1
            last_pres[first_item] = now

            for ts in future:

                item = self._threshold_select(
                    n_pres=n_pres,
                    param=param,
                    n_item=n_item,
                    is_item_specific=is_item_specific,
                    ts=ts, last_pres=last_pres,
                    log_thr=log_thr)

                n_pres[item] += 1
                last_pres[item] = ts

            seen = n_pres > 0
            log_p_seen = self._cp_log_p_seen(
                seen=seen,
                n_pres=n_pres,
                param=param,
                n_item=n_item,
                is_item_specific=is_item_specific,
                last_pres=last_pres,
                ts=eval_ts)

            n_learnt = np.sum(log_p_seen > log_thr)
            if n_learnt == n_item:
                break

            n_item = first_item
            if n_item <= 1:
                break

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

        future_ts, eval_ts = self._get_future_ts(
            now=now, session=session,
            next_sessions=next_sessions,
            eval_time=eval_time)

        n_pres = np.array(learner.n_pres, dtype=int)
        last_pres = np.array(learner.last_pres, dtype=float)

        is_item_specific = len(param.shape) > 1

        log_thr = np.log(self.learnt_threshold)

        item_idx = self._forward(
            param=param,
            future_ts=future_ts,
            eval_ts=eval_ts,
            is_item_specific=is_item_specific,
            n_pres=n_pres,
            last_pres=last_pres,
            log_thr=log_thr)

        return item_idx
