from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import datetime

import numpy as np

from teaching_material.models import Kanji
from learner.models.user import User


class LeitnerManager(models.Manager):

    def create(self, material, delay_factor=2, **kwargs):

        n_item = material.count()
        id_items = [m.id for m in material]
        box = [-1 for _ in range(n_item)]
        due = [None for _ in range(n_item)]

        obj = super().create(n_item=n_item,
                             id_items=id_items,
                             box=box,
                             due=due,
                             delay_factor=delay_factor,
                             **kwargs)

        obj.material.set(material)
        return obj


class Leitner(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)

    delay_factor = models.IntegerField()

    material = models.ManyToManyField(Kanji,
                                      related_name="material")
    n_item = models.IntegerField()
    id_items = ArrayField(models.IntegerField(), default=list)

    box = ArrayField(models.IntegerField(), default=list)
    due = ArrayField(models.DateTimeField(), default=list)

    objects = LeitnerManager()

    class Meta:

        db_table = 'leitner'
        app_label = 'teacher'

    def update_box_and_due_time(self, last_idx,
                                last_was_success, last_time_reply):

        if last_was_success:
            self.box[last_idx] += 1
        else:
            self.box[last_idx] = \
                max(0, self.box[last_idx] - 1)

        delay = self.delay_factor ** self.box[last_idx]
        # Delay is 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 ... minutes
        self.due[last_idx] = \
            last_time_reply + datetime.timedelta(minutes=delay)

    def _pickup_item(self):

        seen = np.argwhere(np.asarray(self.box) >= 0).flatten()
        n_seen = len(seen)

        if n_seen == self.n_item:
            return np.argmin(self.due)

        else:
            seen__due = np.asarray(self.due)[seen]
            print("seen__due", seen__due)
            seen__is_due = np.asarray(seen__due) <= timezone.now()
            print(timezone.now())
            print("seen__is_due", seen__is_due)
            if np.sum(seen__is_due):
                seen_and_is_due__due = seen__due[seen__is_due]

                return seen[seen__is_due][np.argmin(seen_and_is_due__due)]
            else:
                return self._pickup_new()

    def _pickup_new(self):
        return np.argmin(self.box)

    def ask(self):

        last_q_entry = self.question_set.order_by("id").reverse().first()
        if last_q_entry is None:
            print("No previous entry: Present new item!")
            question_idx = self._pickup_new()

        else:
            last_was_success = last_q_entry.success
            last_time_reply = last_q_entry.time_reply
            idx_last_q = self.id_items.index(last_q_entry.item.id)

            self.update_box_and_due_time(
                last_idx=idx_last_q,
                last_was_success=last_was_success,
                last_time_reply=last_time_reply)
            question_idx = self._pickup_item()

        item = self.material.get(id=self.id_items[question_idx])

        self.save()
        return item
