from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from user.models.user import User

import numpy as np
from scipy.special import logsumexp
import scipy.stats as stats


EPS = np.finfo(np.float).eps


class PsychologistManager(models.Manager):

    def create(self, user, n_item, bounds, grid_size, is_item_specific,
               grid_methods):

        gp = self.cp_grid_param(grid_size=grid_size,
                                bounds=bounds, grid_methods=grid_methods)

        n_param_set, n_param = gp.shape
        grid_param = gp.flatten()

        # x = np.linspace(0, 1, grid_size)
        # y = stats.beta.pdf(x, a=1.5, b=5)
        # z = y[::-1, None] * y[None, :]
        # lp = np.zeros(n_param_set)
        # lp[:] = z.flatten()

        lp = np.ones(n_param_set)
        lp -= logsumexp(lp)

        init_guess = np.dot(np.exp(lp), gp)

        n_pres = np.zeros(n_item, dtype=int)

        obj = super().create(
            user=user,
            grid_param=list(grid_param),
            n_param=n_param,
            n_item=n_item,
            bounds=list(np.asarray(bounds).flatten()),
            n_pres=list(n_pres),
            is_item_specific=is_item_specific)

        lp_list = list(lp)
        init_guest_list = list(init_guess)

        if is_item_specific:
            lp_obj = [
                LogPost(user=user, psychologist=obj, value=lp_list,
                        item=i)
                for i in range(n_item)
            ]
            LogPost.objects.bulk_create(lp_obj)

            ep_obj = [
                Param(user=user, psychologist=obj, value=init_guest_list,
                      item=i)
                for i in range(n_item)
            ]
            Param.objects.bulk_create(ep_obj)
        else:
            LogPost.objects.create(value=lp_list, user=user,
                                   psychologist=obj)
            Param.objects.create(value=init_guest_list, user=user,
                                 psychologist=obj)

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
    def cp_grid_param(cls, grid_size, bounds, grid_methods):
        bounds = np.asarray(bounds)
        grid_methods = np.asarray(grid_methods)

        diff = bounds[:, 1] - bounds[:, 0] > 0
        not_diff = np.invert(diff)

        values = np.atleast_2d(
            [m(*b, num=grid_size) for (b, m) in
             zip(bounds[diff], grid_methods[diff])])

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

                log_post = self.logpost_set.get(item=item)

                lp = np.array(log_post.value)
                lp += log_lik
                lp -= logsumexp(lp)

                log_post.value = list(lp)
                log_post.save()

                pr = self.param_set.get(item=item)
                pr.value = list(np.dot(np.exp(lp), gp))
                pr.save()

            else:
                log_post = self.logpost_set.first()

                lp = np.array(log_post.value)
                lp += log_lik
                lp -= logsumexp(lp)

                log_post.value = list(lp)
                log_post.save()

                pr = self.param_set.first()
                pr.value = list(np.dot(np.exp(lp), gp))
                pr.save()
            print("Posterior of parametrization updated")

        self.n_pres[item] += 1
        self.save()

        t2 = timezone.now()
        print(f"Time to update the post dist of parameter values {t2-t1}")

    def inferred_learner_param(self):

        t1 = timezone.now()

        if self.is_item_specific:
            param = np.array(self.param_set.order_by('item')
                             .values_list('value', flat=True))

        else:
            param = np.asarray(self.param_set.first().value)

        t2 = timezone.now()
        print(f"Time to infer the best parameters given post dist {t2-t1}")
        return param


class Param(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)

    item = models.IntegerField(default=None, null=True)

    value = ArrayField(models.FloatField(), default=list)


class LogPost(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)

    item = models.IntegerField(default=None, null=True)

    value = ArrayField(models.FloatField(), default=list)
