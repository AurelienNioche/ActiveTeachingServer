import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pickle
import numpy as np

from user_data.models import User
# from teaching_material.selection import kanji

import analysis.tools.history
import analysis.plot.human
from analysis.fit.fit import DifferentialEvolution

from bot_client.learning_model.act_r.act_r import ActR

from core.fixed_parameters import N_POSSIBLE_REPLIES


BKP_FOLDER = os.path.join("analysis", "data")
os.makedirs(BKP_FOLDER, exist_ok=True)


def main():

    users = User.objects.all().order_by('id')
    n_user = users.count()
    # n_item = len(kanji)

    for i, user in enumerate(users):

        user_id = user.id

        print("-"*16)
        print(f"User {user_id} ({i}/{n_user})")
        print("-" * 16)
        print()
        print("Importing data...", end=' ', flush=True)

        hist_question, hist_success, seen = \
            analysis.tools.history.get(user_id=user_id)
        print("Done.\n")

        print(f"N iteration: {len(hist_question)}.")
        print(f"N kanji seen: {len(np.unique(hist_question))}.")
        print(f"Average success rate: {np.mean(hist_success)*100:.2f}%.")
        print()

        analysis.plot.human.plot(
            seen=seen,
            successes=hist_success,
            extension=f'_u{user_id}'
        )

        print("Running fit...", end=' ', flush=True)
        de = DifferentialEvolution(model=ActR)

        r = de.evaluate(
            hist_question=hist_question,
            hist_success=hist_success,
            task_param={'n_possible_replies': N_POSSIBLE_REPLIES}
        )

        print("Done.\n")

        pickle.dump(r, open(os.path.join(BKP_FOLDER, f'fit_u{user_id}.p'),
                            'wb'))
        print(f'Best param: {r["best_param"]}, '
              f'Best value: {r["best_value"]:.2f}')
        print()


if __name__ == "__main__":

    main()
