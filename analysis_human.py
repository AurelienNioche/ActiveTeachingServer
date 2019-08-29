import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user_data.models import Question, User
from teaching_material.selection import kanji

import analysis.tools.history
import analysis.plot.human
from analysis.fit.fit import DifferentialEvolution

from bot_client.learning_model.act_r.act_r import ActR

from core.fixed_parameters import N_POSSIBLE_REPLIES


def main():

    users = [User.objects.get(id=60,), ]  # User.objects.all().order_by('id')

    n_item = len(kanji)

    for user in users:

        user_id = user.id

        print(f"User {user_id}")
        print("*" * 4)

        hist_question, hist_success, seen = \
            analysis.tools.history.get(user_id=user_id)

        n_iteration = len(hist_question)
        analysis.plot.human.plot(
            seen=seen,
            successes=hist_success
        )

        de = DifferentialEvolution(model=ActR)

        r = de.evaluate(
            hist_question=hist_question,
            hist_success=hist_success,
            task_param={'n_possible_replies': N_POSSIBLE_REPLIES}
        )
        print(r["best_param"], r["best_value"])


if __name__ == "__main__":

    main()
