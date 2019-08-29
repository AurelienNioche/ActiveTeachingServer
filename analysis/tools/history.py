import numpy as np

from user_data.models import Question
from teaching_material.selection import kanji


def get(user_id):

    n_item = len(kanji)

    # Get historic
    entries_question = Question.objects.filter(user_id=user_id).order_by('t')

    assert entries_question.count() > 0, \
        f"Are sure that user {user_id} exists?"

    n_iteration = entries_question.count()

    hist_question = np.zeros(n_iteration, dtype=int)
    hist_success = np.zeros(n_iteration, dtype=bool)
    seen = np.zeros((n_item, n_iteration), dtype=bool)
    for t in range(n_iteration):

        question = entries_question[t].question
        success = entries_question[t].success

        hist_question[t] = question
        hist_success[t] = success

        seen[question, t:] = True
        # print("t", t, "n_seen", np.sum(seen[:, t]))

    return hist_question, hist_success, seen
