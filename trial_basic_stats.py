import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import numpy as np

from bot_client.artificial_learner.act_r import ActR
from bot_client.tools.evaluation import p_recall_over_time_after_learning

from plot.learning_summary import summary

from user_data.models import Question
from teaching_material.models import Kanji


def main():

    user_id = 52

    n_item = len(Kanji.objects.all())

    # Get historic
    entries_question = Question.objects.filter(user_id=user_id).order_by('t')

    n_iteration = 10   # entries_question.count()

    hist_question = np.zeros(n_iteration, dtype=int)
    hist_success = np.zeros(n_iteration, dtype=bool)
    seen = np.zeros((n_item, n_iteration), dtype=bool)
    for t in range(n_iteration):
        hist_question[t] = entries_question[t].question
        hist_success[t] = entries_question[t].success

        seen[entries_question[t], t:] = True
        print("t", t, "n_seen", np.sum(seen[:, t]))

    print(seen)
    print('hist question', hist_question)
    print('hist success', hist_success)

    agent = ActR(
        n_iteration=1000,
        param={"d": 0.5, "tau": 0.01, "s": 0.06}
    )

    p_recall_hist = p_recall_over_time_after_learning(
        agent=agent, n_iteration=n_iteration, n_item=n_item,
    )

    summary(
        p_recall=p_recall_hist,
        seen=seen,
        successes=hist_success,
    )


if __name__ == "__main__":
    main()
