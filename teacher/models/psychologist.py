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
                                        bounds=bounds)
        n_param_set = grid_param.shape[0]
        list_grid_param = list(grid_param.flatten())

        lp = np.ones(n_param_set)
        log_post = lp - logsumexp(lp)
        if heterogeneous_param:
            log_post_all = np.zeros((n_item, n_param_set))
            log_post_all[:] = log_post
            list_log_post = list(log_post_all.flatten())
        else:
            list_log_post = list(log_post)

        obj = super().create(
            learner=learner,
            log_post=list_log_post,
            grid_param=list_grid_param,
        )
        return obj

    @staticmethod
    def cp_grid_param(grid_size, bounds):

        return np.asarray(list(
            product(*[
                np.linspace(*b, grid_size)
                for b in bounds])))


class Psychologist(models.Model):

    learner = models.OneToOneField(Learner, on_delete=models.CASCADE)
    grid_param = ArrayField(models.FloatField(), default=list)
    log_post = ArrayField(models.FloatField(), default=list)

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
            if self.learner.heterogeneous_param:
                log_post = np.reshape(self.log_post, (self.learner.n_item, -1))
                lp = log_post[item]
            else:
                lp = np.asarray(self.log_post)

            lp += log_lik
            lp -= logsumexp(lp)

            if self.learner.heterogeneous_param:
                log_post[item] = lp
                self.log_post = list(log_post.flatten())
            else:
                self.log_post = list(lp)

            self.save()

        self.learner.update(item=item, timestamp=timestamp)

    def p_seen(self):

        gp = np.reshape(self.grid_param, (-1, self.learner.n_param))
        if self.learner.heterogeneous_param:

            param = np.zeros((self.learner.n_item, self.learner.n_param))
            param[:] = self.get_init_guess(self.learner.bounds)
            lp = np.reshape(self.log_post, (self.learner.n_item, -1))
            rep = np.asarray(self.learner.n_pres) > 1
            param[rep] = gp[lp[rep].argmax(axis=-1)]
        else:
            if np.max(self.learner.n_pres) <= 1:
                param = self.get_init_guess(self.learner.bounds)
            else:
                param = gp[np.argmax(self.log_post)]

        return self.learner.p_seen(param=param)

    @staticmethod
    def get_init_guess(bounds):
        bounds = np.reshape(bounds, (-1, 2))
        return [np.mean(b) for b in bounds]
