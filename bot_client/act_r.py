import numpy as np

from . artificial_learner.act_r import ActR
from . basic import MySocket


class ActRSocket(MySocket, ActR):

    def __init__(
            self,
            param,
            n_iteration=10,
            waiting_time=1,
            hist=None,
            t=None,
            n_possible_replies=None):

        MySocket.__init__(self, waiting_time=waiting_time)
        ActR.__init__(self, n_possible_replies=n_possible_replies,
                      n_iteration=n_iteration,
                      param=param, hist=hist, t=t)

    def decide(self, id_possible_replies, id_question, id_correct_answer):

        recall = self.recall(item=id_question)

        self.learn(item=id_question)
        if recall:
            return id_correct_answer
        else:
            return np.random.choice(id_possible_replies)
