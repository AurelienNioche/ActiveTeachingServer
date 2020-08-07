from django.db import models
from django.contrib.postgres.fields import ArrayField

from user.models.user import User

import numpy as np
from scipy.special import expit
import math

EPS = np.finfo(np.float).eps


class Walsh2018Manager(models.Manager):

    def create(self, user, n_item):

        obj = super().create(user=user, n_item=n_item,
                             seen=list(np.zeros(n_item)))
        return obj


class Walsh2018(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()

    seen = ArrayField(models.BooleanField(), default=list)

    ts = ArrayField(models.BigIntegerField(), default=list)
    hist = ArrayField(models.IntegerField(), default=list)

    n_seen = models.IntegerField(default=0)
    seen_item = ArrayField(models.IntegerField(), default=list)

    objects = Walsh2018Manager()

    class Meta:

        db_table = 'walsh'
        app_label = 'teaching'

    def p(self, item, param, now, hist, ts):

        self.set_param(param=param)

        relevant = hist == item
        rep = ts[relevant]
        n = len(rep)
        delta = (now - rep)

        if n == 0:
            return 0
        elif np.min(delta) == 0:
            return 1
        else:

            w = delta ** -self.x
            w /= np.sum(w)

            _t_ = np.sum(w * delta)
            if n > 1:
                lag = rep[1:] - rep[:-1]
                d = self.b + self.m * np.mean(1/np.log(lag + math.e))
            else:
                d = self.b

            _m_ = n ** self.c * _t_ ** -d

            v = (-self.tau + _m_) / self.s
            p = expit(v)
            return p

    def p_seen(self, param, now):

        return self.p_seen_spec_hist(
            param=param, now=now, hist=self.hist, ts=self.ts)

    def p_seen_spec_hist(self, param, now, hist, ts):

        self.set_param(param=param)

        seen = np.zeros(self.n_item, dtype=bool)
        seen[np.unique(hist)] = True

        ts = np.asarray(ts)
        hist = np.asarray(hist)

        n_seen = np.sum(seen)
        n = np.zeros(n_seen)
        _t_ = np.zeros(n_seen)
        mean_lag = np.zeros(n_seen)

        for i_it, item in enumerate(np.flatnonzero(seen)):

            is_item = hist == item
            rep = ts[is_item]

            n_it = len(rep)

            delta = (now - rep)

            w = delta ** -self.x
            w /= np.sum(w)

            _t_it = np.sum(w * delta)

            _t_[i_it] = _t_it
            n[i_it] = n_it

            if n_it > 1:
                lag = rep[1:] - rep[:-1]
                mean_lag[i_it] = np.mean(1 / np.log(lag + math.e))

        one_view = n == 1
        more_than_one = np.invert(one_view)
        _m_ = np.zeros(n_seen)
        _m_[one_view] = _t_[one_view] ** - self.b
        _m_[more_than_one] = n[more_than_one] ** self.c \
            * _t_[more_than_one] ** - (self.b + self.m * mean_lag[more_than_one])

        with np.errstate(divide="ignore", invalid="ignore"):
            v = (-self.tau + _m_) / self.s
            p = expit(v)
        return p, seen

    def log_lik_grid(self, item, grid_param, response, timestamp):
        p = np.zeros(len(grid_param))
        hist = np.asarray(self.hist)
        ts = np.asarray(self.ts)
        for i, param in enumerate(grid_param):
            p[i] = self.p(item=item, param=param, now=timestamp,
                          hist=hist, ts=ts)
        p = p if response else 1 - p
        return np.log(p+EPS)

    @staticmethod
    def log_lik(param, hist, success, timestamp):
        if isinstance(param, dict):
            tau, s, b, m, c, x = \
                param["tau"], param["s"], param["b"], \
                param["m"], param["c"], param["x"]
        else:
            tau, s, b, m, c, x = param

        _m_ = np.zeros(len(hist))

        for item in np.unique(hist):

            is_item = hist == item
            rep = timestamp[is_item]
            n = len(rep)

            _m_item = np.zeros(n)

            _m_item[0] = - np.inf  # To adapt for xp
            if n > 1:
                _m_item[1] = (rep[1]-rep[0])**-b
            for i in range(2, n):
                delta = rep[i] - rep[:i]

                w = delta ** -x
                w /= np.sum(w)

                _t_ = np.sum(w * delta)

                lag = rep[1:i+1] - rep[:i]
                d = b + m * np.mean(1 / np.log(lag + math.e))
                _m_item[i] = i ** c * _t_ ** -d

            _m_[is_item] = _m_item

        with np.errstate(divide="ignore", invalid="ignore"):
            v = (-tau + _m_) / s

        p = expit(v)
        failure = np.invert(success)
        p[failure] = 1 - p[failure]
        # print("hist", hist, "success", success)
        # print("param", param, "p", p)
        log_lik = np.log(p + EPS)
        return log_lik.sum()

    def update(self, idx_last_q, last_time_reply):

        self.seen[idx_last_q] = True
        self.hist.append(idx_last_q)
        self.ts.append(last_time_reply)

        self.n_seen = np.sum(self.seen)
        self.seen_item = list(np.flatnonzero(self.seen))

        self.save()

    def set_param(self, param):

        if isinstance(param, dict):
            for k, v in param.items():
                setattr(self, k, v)
        else:
            self.tau, self.s, self.b, self.m, self.c, self.x = param
