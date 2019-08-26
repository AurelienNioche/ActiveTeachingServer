import numpy as np

from teacher.metaclass import GenericTeacher


class Leitner(GenericTeacher):

    def __init__(self, delay_factor=2, **kwargs):
        """
        :param normalize_similarity: bool.
            Normalized description of
            semantic and graphic connections between items
        :param delay_factor:
        :param verbose:
            displays each question asked and replies at each
            iteration
        :var self.taboo:
            integer value in range(0 to n_items). Index of the item
            shown in previous iteration.
        :var self.learning_progress:
            array of size n_item representing the box
            number of i^th item at i^th index.
        :var self.wait_time_arr:
            array of size n_item representing the waiting time
            of i^th item at i^th index.
        """

        super().__init__(**kwargs)

        self.delay_factor = delay_factor
        self.learning_progress = np.zeros(self.n_item)
        self.wait_time_arr = np.zeros(self.n_item)

        self.taboo = None

    def modify_sets(self, hist_success, t):
        """
        :param t: time step (integer)
        :param hist_success: list of booleans (True: success, False: failure)
        for every question

        The boxes will be modified according to the following rules:
            * Move an item to the next box for a successful reply by learner
            * Move an item to the previous box for a failure.
        """
        taboo = self.taboo
        prev_box = self.learning_progress[taboo]
        if hist_success[t-1]:
            self.learning_progress[taboo] += 1
        else:
            if prev_box > 0:
                self.learning_progress[taboo] -= 1

    def update_wait_time(self):
        """
        Update the waiting time of every item in wait_time_arr according to the
         following rules:
            * Taboo will have its wait time changed according to its box.
            * The rest of the item's wait time will be increased by 1
        """

        for i in range(self.n_item):
            if i != self.taboo:
                self.wait_time_arr[i] += 1
            else:
                taboo_box = self.learning_progress[self.taboo]
                self.wait_time_arr[self.taboo] = -(taboo_box *
                                                   self.delay_factor)

    def find_due_items(self):
        """
        :return: arr : array that contains the items that are due to be shown
        Pick all items with positive waiting time.

        Suppose there exist no due item then pick all items except taboo.
        """
        result = np.where(self.wait_time_arr > 0)
        arr = result[0]
        if len(arr) == 0:
            complete_arr = np.arange(self.n_item)
            arr = np.delete(complete_arr, self.taboo)
        return arr

    @staticmethod
    def find_due_seen_items(due_items, hist_item):
        """
        :param due_items: array that contains items that are due to be shown
        :param hist_item: historic of presented items
        :var seen_due_items: integer array with size of due_items
                * Contains the items that have been seen
                    at least once and are due to be shown.
        :return: * seen_due_items: as before
                * count: the count of the number of items in seen__due_items

        Finds the items that are seen and are due to be shown.
        """

        seen_due_items = np.intersect1d(hist_item, due_items)
        count = len(seen_due_items)

        if count == 0:
            seen_due_items = due_items
            count = len(due_items)
        return seen_due_items, count

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
            wait_time_item = self.wait_time_arr[items_arr[i]]
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
            box = self.learning_progress[item]
            if box < min_box:
                items_arr = [item]
                min_box = box
            elif box == min_box:
                items_arr.append(item)
        assert len(items_arr), 'This should not be empty'

        return items_arr

    def _get_next_node(self, t, hist_success, hist_item, **kwargs):
        """
        :return: integer (index of the question to ask)

        Every item is associated with:
            * A waiting time i.e the time since it was last shown to the learner.
                -- maintained in variable wait_time_arr
            * A box that decides the frequency of repeating an item.
                -- maintained in variable learning_progress
        Function implements 4 rules in order:
            1. The items that are due to be shown are picked.
            2. Preference given to the seen items.
            3. Preference given to the items present in lowest box number.
            4. Randomly pick from the said items.

        """
        if t == 0:
            # No past memory, so a random question shown from learning set
            random_question = np.random.randint(0, self.n_item)
            self.taboo = random_question
            return int(random_question)

        self.modify_sets(hist_success=hist_success, t=t)
        self.update_wait_time()

        # Criteria 1, get due items
        due_items = self.find_due_items()

        # preference for seen item
        seen_due_items, count = self.find_due_seen_items(
            due_items=due_items, hist_item=hist_item)

        # items with maximum waiting time
        max_overdue_items = self.find_max_waiting(seen_due_items[:count])

        # pick item in lowest box
        least_box_items = self.pick_least_box(max_overdue_items)

        if len(least_box_items) > 1:
            pick_question_index = np.random.randint(len(least_box_items))
            new_question = least_box_items[pick_question_index]
        else:
            new_question = least_box_items[0]

        self.taboo = new_question
        return new_question
