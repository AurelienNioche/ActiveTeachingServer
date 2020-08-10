import numpy as np

from . generic import Learner


EPS = np.finfo(np.float).eps


class ExponentialNDelta(Learner):

    def __init__(self, param):

        self.n_pres = dict()
        self.last_pres = dict()

        super().__init__(param)

    def p(self, question_id, timestamp, is_item_specific=False):

        if question_id not in self.n_pres:
            return 0

        if is_item_specific:
            init_forget = self.param[question_id, 0]
            rep_effect = self.param[question_id, 1]
        else:
            init_forget, rep_effect = self.param

        fr = init_forget * (1 - rep_effect) ** (self.n_pres[question_id] - 1)

        delta = timestamp - self.last_pres[question_id]
        return np.exp(- fr * delta)

    def update(self, question_id, timestamp):

        self.last_pres[question_id] = timestamp

        if question_id in self.n_pres:
            self.n_pres[question_id] += 1
        else:
            self.n_pres[question_id] = 1
