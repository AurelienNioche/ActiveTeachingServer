import os
import pickle

import numpy as np

from teaching_material.selection import kanji
from user_data.models import Question

BKP_FOLDER = os.path.join("data", "Pilot20190902", "pickle", "history")
os.makedirs(BKP_FOLDER, exist_ok=True)


def get(user_id):

    bkp_file = os.path.join(BKP_FOLDER, f"user_{user_id}.p")

    if os.path.exists(bkp_file):

        print("Loading from pickle file...")
        hist_question, hist_success, seen = \
            pickle.load(open(bkp_file, 'rb'))
        return hist_question, hist_success, seen

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

    pickle.dump((hist_question, hist_success, seen),
                open(bkp_file, 'wb'))

    return hist_question, hist_success, seen
