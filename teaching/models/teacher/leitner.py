from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime

import numpy as np


class LeitnerManager(models.Manager):

    def create(self, material, delay_factor, delay_min, user):

        n_item = material.count()
        id_items = [m.id for m in material]
        box = [-1 for _ in range(n_item)]
        due = [None for _ in range(n_item)]

        obj = super().create(n_item=n_item,
                             id_items=id_items,
                             box=box,
                             due=due,
                             delay_min=delay_min,
                             delay_factor=delay_factor,
                             user=user)

        obj.material.set(material)
        return obj


class Leitner(models.Model):

    delay_factor = models.IntegerField()
    delay_min = models.IntegerField()

    n_item = models.IntegerField()

    box = ArrayField(models.IntegerField(), default=list)
    due = ArrayField(models.BigIntegerField(), default=list)

    objects = LeitnerManager()

    class Meta:

        db_table = 'leitner'
        app_label = 'teacher'

    def _update_box_and_due_time(
            self, last_idx, last_was_success, last_time_reply):

        if last_was_success:
            self.box[last_idx] += 1
        else:
            self.box[last_idx] = \
                max(0, self.box[last_idx] - 1)

        delay = self.delay_min * self.delay_factor ** self.box[last_idx]
        # Delay is 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 ...
        # multiplied by delay_min seconds
        self.due[last_idx] = last_time_reply + delay

    def _pickup_item(self, now):

        seen = np.argwhere(np.asarray(self.box) >= 0).flatten()
        n_seen = len(seen)

        if n_seen == self.n_item:
            return np.argmin(self.due)

        else:
            seen__due = np.asarray(self.due)[seen]
            seen__is_due = np.asarray(seen__due) <= now
            if np.sum(seen__is_due):
                seen_and_is_due__due = seen__due[seen__is_due]

                return seen[seen__is_due][np.argmin(seen_and_is_due__due)]
            else:
                return self._pickup_new()

    def _pickup_new(self):
        return np.argmin(self.box)

    def update(self, idx_last_q, last_was_success, last_time_reply):

        self._update_box_and_due_time(
            last_idx=idx_last_q,
            last_was_success=last_was_success,
            last_time_reply=last_time_reply)
        self.save()

    def ask(self, now):
        return self._pickup_item(now)
