import numpy as np

from . basic import MySocket


class LearnerSocket(MySocket):

    def __init__(
            self,
            cognitive_model,
            waiting_time=1,
            n_iteration=10,
            **kwargs):

        MySocket.__init__(self, waiting_time=waiting_time,
                          n_iteration=n_iteration)
        self.learner = cognitive_model(n_iteration=n_iteration, **kwargs)

    def decide(self, id_possible_replies, id_question, id_correct_answer):

        recall = self.learner.p_recall(item=id_question) > np.random.random()

        self.learner.learn(item=id_question)
        if recall:
            return id_correct_answer
        else:
            return np.random.choice(id_possible_replies)
