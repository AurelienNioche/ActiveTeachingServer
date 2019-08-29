import numpy as np

from user_data.models import Question


def get(user_id):

    # Get historic
    entries = Question.objects.filter(user_id=user_id).order_by('t')

    assert entries.count() > 0, \
        f"Are sure that user {user_id} exists?"

    n_iteration = entries.count()

    hist_reaction_time = np.zeros(n_iteration, dtype=int)
    for t in range(n_iteration):

        reaction_time = int(
            (entries[t].time_reply -
             entries[t].time_display).total_seconds() * 10 ** 3
        )

    return hist_reaction_time
