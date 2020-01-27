from django.db import models
from django.contrib.postgres.fields import ArrayField

from learner.models import User
from teaching_material.models import Kanji

# Create your models here.
import numpy as np


from django.db import models


class LeitnerManager(models.Manager):

    def create(self, material, **kwargs):
        # Do some extra stuff here on the submitted data before saving...

        # Now call the super method which does the actual creation
        obj = super().create(n_item=len(material), **kwargs)
        for m in material:
            obj.material.add(m)

        # obj.save()
        return obj


class Leitner(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)

    delay_factor = models.IntegerField(default=2)
    box_min = models.IntegerField(default=1)
    n_item = models.IntegerField(default=-1)
    taboo = models.IntegerField(default=-1)

    # Material
    material = models.ManyToManyField(Kanji,
                                      related_name="material")

    # array of size n_item representing the box
    #             number of i^th item at i^th index.
    box = ArrayField(models.IntegerField(), default=list)

    #  array of size n_item representing the waiting time
    #             of i^th item at i^th index.
    waiting_time = ArrayField(models.IntegerField(), default=list)

    seen = ArrayField(models.BooleanField(), default=list)

    objects = LeitnerManager()

    class Meta:

        db_table = 'leitner'
        app_label = 'teacher'

    def modify_sets(self, last_was_success):
        """
        :param last_was_success: bool

        The boxes will be modified according to the following rules:
            * Move an item to the next box for a successful reply by learner
            * Move an item to the previous box for a failure.
        """
        if last_was_success:
            self.box[self.taboo] += 1
        elif self.box[self.taboo] > self.box_min:
            self.box[self.taboo] -= 1

    def update_wait_time(self):
        """
        Update the waiting time of every item in wait_time_arr according to the
         following rules:
            * Taboo will have its wait time changed according to its box.
            * The rest of the item's wait time will be increased by 1
        """

        for i in range(self.n_item):
            if i != self.taboo:
                self.waiting_time[i] += 1
            else:
                self.waiting_time[self.taboo] \
                    = - self.delay_factor**self.box[self.taboo]

    def find_due_items(self):
        """
        :return: arr : array that contains bool
        True := the item is due to be shown

        Suppose there exist no due item then pick all items except taboo.
        """
        due = np.asarray(self.waiting_time) > 0
        if np.sum(due) == 0:
            due = np.ones(self.n_item)

        due[self.taboo] = 0
        return due

    def find_due_seen_items(self, due):
        """
        :param due: bool array size N
        :return: seen_due: bool array size N
            True := the items has been seen
                    at least once and are due to be shown

        Finds the items that are seen and are due to be shown.
        """

        seen_due = due * np.asarray(self.seen)

        if np.sum(seen_due) == 0:
            return due
        else:
            return seen_due

    def find_max_waiting(self, items_arr):
        """
        :param items_arr: an integer array that contains the items that should
                be shown.
        :return: arr: contains the items that have been waiting to be shown the
            most.

        Finds those items with maximum waiting time.
        """

        max_wait = float('-inf')
        arr = None
        for i in range(len(items_arr)):
            wait_time_item = self.waiting_time[items_arr[i]]
            if max_wait < wait_time_item:
                arr = [items_arr[i]]
                max_wait = wait_time_item
            elif max_wait == wait_time_item:
                arr.append(items_arr[i])
        return arr

    def pick_least_box(self, max_overdue_items):
        """
        :param max_overdue_items: an integer array that contains the items that
            should be shown.
        :return: items_arr: contains the items that are in the lowest box from
            the max_overdue_items.

        Finds the items present in the lowest box number.
        """

        items_arr = []
        min_box = float('inf')
        for item in max_overdue_items:
            box = self.box[item]
            if box < min_box:
                items_arr = [item]
                min_box = box
            elif box == min_box:
                items_arr.append(item)
        assert len(items_arr), 'This should not be empty'

        return items_arr

    def ask(self, last_was_success):
        """

        Every item is associated with:
            * A waiting time i.e the time since it was
            last shown to the learner.
                -- maintained in variable wait_time_arr
            * A box that decides the frequency of repeating an item.
                -- maintained in variable learning_progress
        Function implements 4 rules in order:
            1. The items that are due to be shown are picked.
            2. Preference given to the seen items.
            3. Preference given to the items present in lowest box number.
            4. Randomly pick from the said items.

        """

        # If first round
        if True not in self.seen:

            print(self.n_item)
            # Initialize the arrays
            self.box = [0 for _ in range(self.n_item)]
            self.waiting_time = [0 for _ in range(self.n_item)]
            self.seen = [False for _ in range(self.n_item)]

            # No past memory, so a random question shown from learning set
            idx_question = np.random.randint(0, self.n_item)

        else:

            self.modify_sets(last_was_success)
            self.update_wait_time()

            # Criteria 1, get due items
            due = self.find_due_items()

            # preference for seen item
            seen_due = self.find_due_seen_items(due)

            # items with maximum waiting time
            max_overdue_items = \
                self.find_max_waiting(np.arange(self.n_item)[seen_due])

            # pick item in lowest box
            least_box_items = self.pick_least_box(max_overdue_items)

            if len(least_box_items) > 1:
                pick_question_index = np.random.randint(len(least_box_items))
                idx_question = least_box_items[pick_question_index]
            else:
                idx_question = least_box_items[0]

        self.taboo = idx_question
        self.seen[idx_question] = True

        question = self.material.all()[int(idx_question)]
        self.save()

        return question
