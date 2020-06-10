from django.db import models
from django.contrib.postgres.fields import ArrayField

import numpy as np

from teaching_material.models import Kanji
from learner.models.user import User
from teacher.models.psychologist import Psychologist


class ThresholdManager(models.Manager):

    def create(self, user, material, learnt_threshold, bounds, grid_size,
               heterogeneous_param):

        n_item = material.count()
        id_items = [m.id for m in material]
        psychologist = Psychologist.objects.create(
            n_item=n_item,
            bounds=bounds,
            grid_size=grid_size,
            heterogeneous_param=heterogeneous_param)

        obj = super().create(
            user=user,
            n_item=n_item,
            id_items=id_items,
            learnt_threshold=learnt_threshold,
            psychologist=psychologist)

        obj.material.set(material)
        return obj


class Threshold(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    psychologist = models.OneToOneField(Psychologist, on_delete=models.CASCADE)

    material = models.ManyToManyField(Kanji, related_name="threshold_material")
    id_items = ArrayField(models.IntegerField(), default=list)
    n_item = models.IntegerField()

    learnt_threshold = models.FloatField()

    objects = ThresholdManager()

    class Meta:

        db_table = 'threshold'
        app_label = 'teacher'

    def _pickup_new(self):
        return np.argmin(self.psychologist.learner.seen)

    def ask(self):

        last_q_entry = self.question_set.order_by("id").reverse().first()
        if last_q_entry is None:
            print("No previous entry: Present new item!")
            question_idx = self._pickup_new()

        else:
            last_was_success = last_q_entry.success
            last_time_reply = last_q_entry.time_reply
            idx_last_q = self.id_items.index(last_q_entry.item.id)

            self.psychologist.update(item=idx_last_q,
                                     response=last_was_success,
                                     timestamp=last_time_reply)

            seen = self.psychologist.learner.seen
            p = self.psychologist.p_seen()

            min_p = np.min(p)

            if np.sum(seen) == self.n_item or min_p <= self.learnt_threshold:
                question_idx = np.arange(self.n_item)[seen][np.argmin(p)]

            else:
                question_idx = self._pickup_new()

        item = self.material.get(id=self.id_items[question_idx])
        return item
