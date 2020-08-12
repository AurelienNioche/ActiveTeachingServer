import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.test_leitner import TestLeitner
from experimental_condition.models.pilot import Pilot


def main():
    for (email, condition) in (
            ("leitner@test.com", TestLeitner.__name__),
            ("pilot@test.com", Pilot.__name__)
            # ("exp_decay_thr_grid@test.com", Condition.EXP_DECAY_THR_GRID),
            # ("walsh_thr_grid@test.com", Condition.WALSH_THR_GRID),
            # ("exp_decay_samp_grid@test.com", Condition.EXP_DECAY_SAMP_GRID),
            # ("walsh_samp_grid@test.com", Condition.WALSH_SAMP_GRID)
            # ("mcts@test.com", Condition.MCTS),
            # ("mcts_sp@test.com", Condition.MCTS_ITEM_SPECIFIC),
            # ("threshold_sp@test.com", Condition.THRESHOLD_ITEM_SPECIFIC)
    ):

        User.objects.filter(email=email).delete()

        user = sign_up(
            email=email,
            password="1234",
            gender=User.MALE,
            age=33,
            mother_tongue="french",
            other_language="english",
            condition=condition
        )

        if user is not None:
            print("Success!")
        else:
            raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
