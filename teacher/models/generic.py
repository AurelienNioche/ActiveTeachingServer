class GenericTeacher:

    def ask(self,
            t=None,
            hist_success=None,
            hist_question=None,
            task_param=None,
            student_param=None,
            student_model=None,
            questions=None,
            replies=None,
            n_iteration=None):

        return \
            self._get_next_node(
                t=t,
                questions=questions,
                replies=replies,
                n_iteration=n_iteration,
                hist_success=hist_success,
                hist_question=hist_question,
                task_param=task_param,
                student_param=student_param,
                student_model=student_model)

    def _get_next_node(self, **kwargs):
        raise NotImplementedError(f"{type(self).__name__} is a meta-class."
                                  "This method need to be overridden")