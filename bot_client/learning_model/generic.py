class Learner:

    def __init__(self, param):

        self.param = param

    def update(self, question_id, timestamp):
        raise NotImplementedError

    def p(self, question_id, timestamp):
        """Expected return from specific learner: p_r"""
        raise NotImplementedError

    # @classmethod
    # def generate_random_parameters(cls):
    #
    #     return {t[0]: np.random.uniform(t[1], t[2]) for t in cls.bounds}
