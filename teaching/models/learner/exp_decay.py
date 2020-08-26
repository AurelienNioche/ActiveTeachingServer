from django.db import models
from django.contrib.postgres.fields import ArrayField

from user.models.user import User

import numpy as np

EPS = np.finfo(np.float).eps


class ExpDecayManager(models.Manager):

    def create(self, user, n_item, cst_time):

        n_pres = list(np.zeros(n_item, dtype=int))
        last_pres = [None for _ in range(n_item)]
        seen = list(np.zeros(n_item))

        obj = super().create(
            user=user,
            seen=seen,
            n_pres=n_pres,
            last_pres=last_pres,
            n_item=n_item,
            cst_time=cst_time)
        return obj


class ExpDecay(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()
    cst_time = models.FloatField()

    seen = ArrayField(models.BooleanField(), default=list)

    ts = ArrayField(models.FloatField(), default=list)
    hist = ArrayField(models.IntegerField(), default=list)

    n_seen = models.IntegerField(default=0)
    seen_item = ArrayField(models.IntegerField(), default=list)

    n_pres = ArrayField(models.IntegerField(), default=list)
    last_pres = ArrayField(models.FloatField(), default=list)

    objects = ExpDecayManager()

    class Meta:

        db_table = 'exp_decay'
        app_label = 'teaching'

    def p_seen(self, param, now):

        seen = np.asarray(self.seen)
        n_pres = np.asarray(self.n_pres)
        last_pres = np.asarray(self.last_pres, dtype=float)
        param = np.asarray(param)

        if len(param.shape) > 1:  # Is item specific
            init_forget = param[seen, 0]
            rep_effect = param[seen, 1]
        else:
            init_forget, rep_effect = param

        fr = init_forget * (1 - rep_effect) ** (n_pres[seen] - 1)

        last_pres = last_pres[seen]
        delta = now - last_pres

        delta *= self.cst_time

        p = np.exp(-fr * delta)
        return p, seen

    def p_seen_spec_hist(self, param, now, hist, ts):

        seen = np.zeros(self.n_item, dtype=bool)
        seen[np.unique(hist)] = True

        param = np.asarray(param)
        hist = np.asarray(hist)
        ts = np.asarray(ts)

        if len(param.shape) > 1:  # Is item specific
            init_forget = param[seen, 0]
            rep_effect = param[seen, 1]
        else:
            init_forget, rep_effect = param

        seen_item = sorted(np.flatnonzero(seen))
        n_pres = np.zeros(self.n_item)
        last_pres = np.zeros(self.n_item)
        for i, item in enumerate(seen_item):
            is_item = hist == item
            n_pres[i] = np.sum(is_item)
            last_pres[i] = np.max(ts[is_item])

        fr = init_forget * (1-rep_effect) ** (n_pres[seen] - 1)

        delta = now - last_pres[seen]
        delta *= self.cst_time

        p = np.exp(-fr * delta)
        return p, seen

    def log_lik_grid(self, item, grid_param, response, timestamp):

        fr = grid_param[:, 0] \
            * (1 - grid_param[:, 1]) ** (self.n_pres[item] - 1)

        delta = timestamp - self.last_pres[item]
        delta *= self.cst_time

        p_success = np.exp(- fr * delta)

        p = p_success if response else 1 - p_success

        log_lik = np.log(p + EPS)
        return log_lik

    def update(self, idx_last_q, last_time_reply):

        self.last_pres[idx_last_q] = last_time_reply
        self.n_pres[idx_last_q] += 1

        self.seen[idx_last_q] = True
        self.hist.append(idx_last_q)
        self.ts.append(last_time_reply)

        self.n_seen = np.sum(self.seen)
        self.seen_item = list(np.flatnonzero(self.seen))

        self.save()
