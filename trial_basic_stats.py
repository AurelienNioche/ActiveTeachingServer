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

from user_data.models import Question


def main():

    user_id = 52

    # Get historic
    entries_question = Question.objects.filter(user_id=user_id).order_by('t')

    hist_question = np.zeros(t, dtype=int)
    hist_success = np.zeros(t, dtype=bool)
    for i, e in enumerate(entries_question):
        hist_question[i] = e.question
        hist_success[i] = e.success

    print('hist question', hist_question)
    print('hist success', hist_success)

    agent = ActR(waiting_time=0,
                    n_iteration=1000,
                    param={"d": 0.5, "tau": 0.01, "s": 0.06})

    p_recall_hist = p_recall_over_time_after_learning(
        agent=agent, n_iteration=n_iteration, n_item=n_item,
    )


if __name__ == "__main__":
    main()