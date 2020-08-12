from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from user.models.user import User

import numpy as np
from scipy.special import logsumexp


EPS = np.finfo(np.float).eps


class PsychologistManager(models.Manager):

    def create(self, user, n_item, bounds, grid_size, is_item_specific,
               init_guess=None):

        gp = self.cp_grid_param(grid_size=grid_size,
                                        bounds=bounds)

        n_param_set, n_param = gp.shape
        grid_param = gp.flatten()

        lp = np.ones(n_param_set)
        lp -= logsumexp(lp)
        if init_guess is None:
            init_guess = np.dot(np.exp(lp), gp)

        if is_item_specific:
            log_post = np.zeros((n_item, n_param_set))
            log_post[:] = lp
            log_post = log_post.flatten()

            ep = np.zeros((n_item, n_param))
            ep[:] = init_guess
            est_param = ep.flatten()
        else:
            log_post = lp
            est_param = init_guess

        n_pres = np.zeros(n_item, dtype=int)

        obj = super().create(
            user=user,
            log_post=list(log_post),
            est_param=list(est_param),
            grid_param=list(grid_param),
            n_param=n_param,
            n_item=n_item,
            bounds=list(np.asarray(bounds).flatten()),
            n_pres=list(n_pres),
            is_item_specific=is_item_specific)
        return obj

    @staticmethod
    def cartesian_product(*arrays):
        la = len(arrays)
        dtype = np.result_type(*arrays)
        arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
        for i, a in enumerate(np.ix_(*arrays)):
            arr[..., i] = a
        return arr.reshape(-1, la)

    @classmethod
    def cp_grid_param(cls, grid_size, bounds):
        bounds = np.asarray(bounds)
        diff = bounds[:, 1] - bounds[:, 0] > 0
        not_diff = np.invert(diff)

        values = np.atleast_2d([np.linspace(*b, num=grid_size)
                                for b in bounds[diff]])
        var = cls.cartesian_product(*values)
        grid = np.zeros((max(1, len(var)), len(bounds)))
        if np.sum(diff):
            grid[:, diff] = var
        if np.sum(not_diff):
            grid[:, not_diff] = bounds[not_diff, 0]

        return grid


class Psychologist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    grid_param = ArrayField(models.FloatField(), default=list)
    log_post = ArrayField(models.FloatField(), default=list)

    n_item = models.IntegerField()
    n_param = models.IntegerField()

    bounds = ArrayField(models.FloatField(), default=list)

    is_item_specific = models.BooleanField()

    n_pres = ArrayField(models.IntegerField(), default=list)

    est_param = ArrayField(models.FloatField(), default=list)

    objects = PsychologistManager()

    class Meta:

        db_table = 'psychologist'
        app_label = 'teaching'

    def update(self, learner, idx_last_q, last_was_success, last_time_reply):

        t1 = timezone.now()

        item = idx_last_q
        response = last_was_success
        timestamp = last_time_reply

        if self.n_pres[item] == 0:
            print("First presentation, no update")
        else:
            gp = np.reshape(self.grid_param, (-1, self.n_param))
            log_lik = learner.log_lik_grid(
                item=item,
                grid_param=gp,
                response=response,
                timestamp=timestamp)

            # Update prior
            if self.is_item_specific:
                log_post = np.reshape(self.log_post, (self.n_item, -1))
                lp = log_post[item]
                lp += log_lik
                lp -= logsumexp(lp)
                log_post[item] = lp
                self.log_post = list(log_post.flatten())

                est_param = np.reshape(self.est_param, (self.n_item, -1))
                est_param[item] = np.dot(np.exp(lp), gp)
                self.est_param = list(est_param.flatten())

            else:
                lp = np.asarray(self.log_post)
                lp += log_lik
                lp -= logsumexp(lp)
                self.log_post = list(lp)

                est_param = np.dot(np.exp(lp), gp)  # gp[np.argmax(self.log_post)]
                self.est_param = list(est_param)
            print("Posterior of parametrization updated")

        self.n_pres[item] += 1
        self.save()

        t2 = timezone.now()
        print(f"Time to update the post dist of parameter values {t2-t1}")

    def inferred_learner_param(self):

        t1 = timezone.now()

        if self.is_item_specific:
            param = np.reshape(self.est_param, (self.n_item, -1))

        else:
            param = np.asarray(self.est_param)

        t2 = timezone.now()
        print(f"Time to infer the best parameters given post dist {t2-t1}")
        return param

