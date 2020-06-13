from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import numpy as np
import pandas as pd

EPS = np.finfo(np.float).eps


class LearnerManager(models.Manager):

    def create(self, n_item, bounds, heterogeneous_param):

        n_pres = np.zeros(n_item, dtype=int)
        last_pres = [None for _ in range(n_item)]

        obj = super().create(
            n_param=len(bounds),
            n_item=n_item,
            bounds=list(np.asarray(bounds).flatten()),
            n_pres=list(n_pres),
            last_pres=last_pres,
            heterogeneous_param=heterogeneous_param)

        return obj


class Learner(models.Model):

    n_param = models.IntegerField()
    n_item = models.IntegerField()
    bounds = ArrayField(models.FloatField(), default=list)
    n_pres = ArrayField(models.IntegerField(), default=list)
    heterogeneous_param = models.BooleanField()
    last_pres = ArrayField(models.DateTimeField(), null=True)

    objects = LearnerManager()

    class Meta:
        db_table = 'learner'
        app_label = 'teacher'

    def update(self, item, timestamp):

        self.last_pres[item] = timestamp
        self.n_pres[item] += 1
        self.save()

    def p(self, item, param=None):

        if self.n_pres[item] == 0:
            return 0

        init_forget, rep_effect = param

        fr = init_forget \
            * (1 - rep_effect) ** (self.n_pres[item] - 1)

        delta = (timezone.now() - self.last_pres[item]).total_seconds()
        p = np.exp(- fr * delta)
        return p

    @property
    def seen(self):
        return np.asarray(self.n_pres) > 0

    def p_seen(self, param):

        seen = np.asarray(self.seen)
        n_pres = np.asarray(self.n_pres)

        if self.heterogeneous_param:
            init_forget = param[seen, 0]
            rep_effect = param[seen, 1]
        else:
            init_forget, rep_effect = param

        fr = init_forget * (1-rep_effect) ** (n_pres[seen] - 1)
        last_pres = pd.Series(self.last_pres)[seen]
        delta_series = timezone.now() - last_pres
        delta = delta_series.dt.total_seconds()
        p = np.exp(-fr * delta)
        return p

    def log_lik(self, item, grid_param, response, timestamp):

        """
        To call before update!!
        """

        fr = grid_param[:, 0] \
            * (1 - grid_param[:, 1]) ** (self.n_pres[item] - 1)

        delta = (timestamp - self.last_pres[item]).total_seconds()
        p_success = np.exp(- fr * delta)

        if response == 1:
            p = p_success
        elif response == 0:
            p = 1 - p_success
        else:
            raise ValueError

        log_lik = np.log(p + EPS)
        return log_lik
