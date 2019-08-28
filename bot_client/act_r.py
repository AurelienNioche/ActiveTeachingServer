from . artificial_learner.act_r import ActR
from . basic import MySocket


class ActRSocket(MySocket, ActR):

    def __init__(
            self,
            n_iteration,
            hist=None,
            t=None,
            n_possible_replies=None,
            param=None):

        MySocket().__init__()
        ActR.__init__(n_possible_replies=n_possible_replies,
                      n_iteration=n_iteration,
                      param=param, hist=hist, t=t)

    def decide(self, id_possible_replies, id_question, id_correct_answer):



        recall = ActR.recall(item=item, po)
