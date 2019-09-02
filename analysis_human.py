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
from analysis.fit.scipy import DifferentialEvolution, Minimize
from analysis.fit.pygpgo import PyGPGO

from bot_client.learning_model.act_r.act_r import ActR
from bot_client.learning_model.act_r.custom import ActRMeaning, ActRGraphic
from teaching_material.selection import kanji, meaning
from core.fixed_parameters import N_POSSIBLE_REPLIES
import analysis.similarity.graphic.measure
import analysis.similarity.semantic.measure

BKP_FOLDER = os.path.join("analysis", "data")
os.makedirs(BKP_FOLDER, exist_ok=True)


def main():

    # Get similarity
    print("Computing the graphic connection...")
    graphic_connection = \
        analysis.similarity.graphic.measure.get(kanji_list=kanji)

    semantic_connection = \
        analysis.similarity.semantic.measure.get(word_list=meaning)

    fit_class = Minimize   # DifferentialEvolution or PyGPO
    list_model_to_fit = ActRMeaning, ActRGraphic, ActR

    task_param = {'n_possible_replies': N_POSSIBLE_REPLIES,
                  'semantic_connection': semantic_connection,
                  'graphic_connection': graphic_connection}

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

        for model_to_fit in list_model_to_fit:
            print(f"Running fit {model_to_fit.__name__}...",
                  end=' ', flush=True)
            de = fit_class(model=model_to_fit)

            r = de.evaluate(
                hist_question=hist_question,
                hist_success=hist_success,
                task_param=task_param
            )

            print("Done.\n")

            pickle.dump(r,
                        open(os.path.join(
                            BKP_FOLDER,
                            f'fit_u{user_id}_{model_to_fit.__name__}.p'),
                            'wb'))
            print(f'Best param: {r["best_param"]}, '
                  f'Best value: {r["best_value"]:.2f}')
            print()


if __name__ == "__main__":

    main()
