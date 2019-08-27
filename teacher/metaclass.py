import numpy as np


class GenericTeacher:

    @classmethod
    def ask(cls,
            t=None,
            hist_success=None,
            hist_questions=None,
            task_param=None,
            student_param=None,
            student_model=None,
            n_item=None,
            n_iteration=None,
            n_possible_replies=None):

        question = \
            cls._get_next_node(
                t=t,
                n_item=n_item,
                n_iteration=n_iteration,
                hist_success=hist_success,
                hist_questions=hist_questions,
                task_param=task_param,
                student_param=student_param,
                student_model=student_model)

        if n_possible_replies:
            poss_rep = self._get_possible_replies(
                item, n_item=n_item, n_possible_replies=n_possible_replies)
            return item, poss_rep
        else:
            return item

    @classmethod
    def _get_next_node(cls, **kwargs):
        raise NotImplementedError(f"{type(cls).__name__} is a meta-class."
                                  "This method need to be overridden")

    @staticmethod
    def _get_possible_replies(question, n_item, n_possible_replies):

        # Select randomly possible replies, including the correct one
        all_replies = list(range(n_item))
        all_replies.remove(item)

        possible_replies = \
            [item, ] + list(np.random.choice(
                all_replies, size=n_possible_replies-1, replace=False))
        possible_replies = np.array(possible_replies)
        np.random.shuffle(possible_replies)
        return possible_replies
