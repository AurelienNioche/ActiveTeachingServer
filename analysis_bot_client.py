import os

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from bot_client.learning_model.act_r import ActR
from analysis.tools import artificial
from analysis.tools import history
import analysis.plot.artificial as plot_artificial

# from user_data.models import Question
from teaching_material.selection import kanji


def main():

    user_id = 60

    n_item = len(kanji)

    hist_question, hist_success, seen = history.get(user_id=user_id)
    n_iteration = len(hist_question)

    # Train the artificial agent
    agent = ActR(
        n_iteration=n_iteration,
        param={"d": 0.5, "tau": 0.01, "s": 0.06}
    )
    for t in range(n_iteration):
        agent.learn(item=hist_question[t])

    p_recall_hist = artificial.p_recall_over_time_after_learning(
        agent=agent, n_iteration=n_iteration, n_item=n_item,
    )

    plot_artificial.plot(
        p_recall=p_recall_hist,
        seen=seen,
        successes=hist_success,
        normalize=False,
    )


if __name__ == "__main__":
    main()
