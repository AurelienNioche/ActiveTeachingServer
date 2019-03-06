import os
import sys
import numpy as np

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import Kanji, User, Parameter, PredefinedTask

from task.parameters import n_possible_replies



def main(n_kanji=10, grade=1):

    # Seed
    np.random.seed(123)

    # Select n kanji among first grade
    k = list(Kanji.objects.filter(grade=grade))

    while True:

        # Select randomly n kanji
        kanji_idx = np.random.choice(np.arange(len(k)), size=n_kanji, replace=False)

        # Get the meaning
        meaning = [k[kanji_idx[i]].meaning for i in range(n_kanji)]

        # Ensure that each kanji has a different meaning
        if len(np.unique(meaning)) == len(meaning):
            break

    # Get the kanji
    kanji = [k[kanji_idx[i]].kanji for i in range(n_kanji)]

    # Get t_max
    t_max = Parameter.objects.get(name='t_max').value

    # Define probability for a kanji to be selected
    p = np.random.random(n_kanji)
    p /= p.sum()

    q_idx = np.random.choice(np.arange(n_kanji), p=p, replace=True)

    for t in t_max:

        # Get question and correct answer
        question = kanji[q_idx[t]]
        correct_answer = meaning[q_idx[t]]

        # Select possible replies
        possible_replies = [correct_answer, ] + \
            np.random.choice(meaning.copy().remove(correct_answer),
                             size=n_possible_replies-1, replace=False)

        # Randomize the order of possible replies
        np.random.shuffle(possible_replies)

        # Create new entry
        q = PredefinedTask()
        q.question = question
        q.correct_answer = correct_answer
        for i in range(n_possible_replies):
            setattr(q, f'possible_reply_{i}', possible_replies[i])

        q.save()


if __name__ == "__main__":
    main()
