import numpy as np

from . random_socket import RandomSocket


class LearnerSocket(RandomSocket):

    def __init__(
            self,
            cognitive_model,
            param,
            url="ws://localhost:8001/",
            email="leitner@test.com",
            password='1234',
            gender='male',
            mother_tongue='french',
            other_language='english',
            waiting_time=1):

        RandomSocket.__init__(self, waiting_time=waiting_time, url=url,
                              email=email, password=password,
                              gender=gender, mother_tongue=mother_tongue,
                              other_language=other_language)
        self.learner = cognitive_model(param)

    def decide(self, id_possible_replies, id_question, id_correct_reply,
               time_display, time_reply):

        p = self.learner.p(question_id=id_question,
                           timestamp=time_display.timestamp())

        self.learner.update(question_id=id_question,
                            timestamp=time_reply.timestamp())
        if p > np.random.random():
            return id_correct_reply
        else:
            return np.random.choice(id_possible_replies)
