import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pickle
import numpy as np

# from user_data.models import User
# from teaching_material.selection import kanji

import analysis.tools.history
import analysis.tools.users
import analysis.plot.human
from analysis.fit.scipy import Minimize # DifferentialEvolution
# from analysis.fit.pygpgo import PyGPGO

from bot_client.learning_model.act_r.act_r import ActR
from bot_client.learning_model.act_r.custom import ActRMeaning, ActRGraphic
from bot_client.learning_model.rl import QLearner
from bot_client.learning_model.hopfield_network.carlos_hopfield import Hopfield
from teaching_material.selection import kanji, meaning
from core.fixed_parameters import N_POSSIBLE_REPLIES
import analysis.similarity.graphic.measure
import analysis.similarity.semantic.measure
from analysis.fit.degenerate import Degenerate


BKP_FOLDER = os.path.join("data", "Pilot20190902", "pickle", "fit")
os.makedirs(BKP_FOLDER, exist_ok=True)


def main():

    # Get similarity
    print("Computing the graphic connection...")
    graphic_connection = \
        analysis.similarity.graphic.measure.get(kanji_list=kanji)

    semantic_connection = \
        analysis.similarity.semantic.measure.get(word_list=meaning)

    fit_class = Minimize   # DifferentialEvolution or PyGPO
    list_model_to_fit = QLearner,  ActR, ActRMeaning, ActRGraphic

    task_param = {
        'n_possible_replies': N_POSSIBLE_REPLIES,
        'n_item': len(semantic_connection),
        'semantic_connection': semantic_connection,
        'graphic_connection': graphic_connection}

    list_user_id = analysis.tools.users.get(force=True)

    # list_user_id = [list_user_id[-1], ]

    n_user = len(list_user_id)
    # n_item = len(kanji)

    for i, user_id in enumerate(list_user_id):

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

        bkp_file = os.path.join(
            BKP_FOLDER,
            f'fit_u{user_id}_degenerate.p')

        if not os.path.exists(bkp_file):

            f = Degenerate()
            r = f.evaluate(
                hist_question=hist_question,
                hist_success=hist_success,
                task_param=task_param)
            pickle.dump(r, open(bkp_file, 'wb'))
        else:
            r = pickle.load(open(bkp_file, 'rb'))

        print('Degenerate model with only success:')
        print(f'Best value: {r["best_value"]:.2f}.\n')

        for model_to_fit in list_model_to_fit:

            bkp_file = os.path.join(
                BKP_FOLDER,
                f'fit_u{user_id}_{model_to_fit.__name__}.p')

            if not os.path.exists(bkp_file):
                print(f"Running fit {model_to_fit.__name__}...",
                      end=' ', flush=True)
                f = fit_class(model=model_to_fit)

                r = f.evaluate(
                    hist_question=hist_question,
                    hist_success=hist_success,
                    task_param=task_param
                )

                print("Done.")

                pickle.dump(r, open(bkp_file, 'wb'))

            else:
                print("Loading from pickle file...", end=' ', flush=True)
                r = pickle.load(open(bkp_file, 'rb'))
                print("Done")

            print(f'Best param: {r["best_param"]}, '
                  f'best value: {r["best_value"]:.2f}.')
            print()


if __name__ == "__main__":

    main()
