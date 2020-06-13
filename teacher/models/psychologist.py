from django.db import models
from django.contrib.postgres.fields import ArrayField

import numpy as np
from scipy.special import logsumexp
from itertools import product

from teacher.models.learner import Learner

EPS = np.finfo(np.float).eps


class PsychologistManager(models.Manager):

    def create(self, n_item, bounds, grid_size, heterogeneous_param):

        learner = Learner.objects.create(
            n_item=n_item, bounds=bounds,
            heterogeneous_param=heterogeneous_param)

        grid_param = self.cp_grid_param(grid_size=grid_size,
                                        bounds=learner.bounds)
        n_param_set = len(grid_param)
        lp = np.ones(n_param_set)
        log_post = lp - logsumexp(lp)

        argmax_post = self.get_init_guess(bounds=learner.bounds)

        obj = super().create(
            learner=learner,
            log_post=list(log_post),
            grid_param=list(grid_param.flatten()),
            argmax_post=list(argmax_post)
        )
        return obj

    @staticmethod
    def get_init_guess(bounds):
        bounds = np.reshape(bounds, (-1, 2))
        return [np.mean(b) for b in bounds]

    @staticmethod
    def cp_grid_param(grid_size, bounds):

        bounds = np.reshape(bounds, (-1, 2))
        return np.asarray(list(
            product(*[
                np.linspace(*b, grid_size)
                for b in bounds])))


class Psychologist(models.Model):

    learner = models.OneToOneField(Learner, on_delete=models.CASCADE)
    grid_param = ArrayField(models.FloatField(), default=list)
    log_post = ArrayField(models.FloatField(), default=list)
    argmax_post = ArrayField(models.FloatField(), default=list)

    objects = PsychologistManager()

    def update(self, item, response, timestamp):

        if self.learner.n_pres[item] == 0:
            pass
        else:
            gp = np.reshape(self.grid_param, (-1, self.learner.n_param))
            log_lik = self.learner.log_lik(item=item,
                                           grid_param=gp,
                                           response=response,
                                           timestamp=timestamp)
            # Update prior
            lp = np.asarray(self.log_post)
            lp += log_lik
            lp -= logsumexp(lp)
            self.log_post = list(lp)

            # Save argmax
            self.argmax_post = list(gp[np.argmax(self.log_post)])
            self.save()

        self.learner.update(item=item, timestamp=timestamp)

    def p_seen(self):
        return self.learner.p_seen(param=self.argmax_post)
