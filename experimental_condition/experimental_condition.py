from django.utils import timezone
import datetime

class Condition:
    TEST = 0


def user_creation(user):

    from teacher.models.leitner import Leitner
    from teacher.models.threshold import Threshold
    from teacher.models.mcts import MCTSTeacher
    from teaching_material.models import Kanji

    if user.condition == Condition.TEST:

        is_item_specific = False
        learnt_threshold = 0.90
        bounds = ((0.001, 0.04), (0.2, 0.5))
        grid_size = 20

        material = Kanji.objects.all()
        Leitner.objects.create(user=user,
                               material=material[0:50],
                               delay_factor=2)
        Threshold.objects.create(user=user,
                                 material=material[50:100],
                                 learnt_threshold=learnt_threshold,
                                 is_item_specific=is_item_specific,
                                 bounds=bounds,
                                 grid_size=grid_size)

        MCTSTeacher.objects.create(user=user,
                                   material=material[100:151],
                                   learnt_threshold=learnt_threshold,
                                   bounds=bounds,
                                   grid_size=grid_size,
                                   is_item_specific=is_item_specific,
                                   iter_limit=500,
                                   time_limit=None,
                                   horizon=10,
                                   time_per_iter=2)

    else:
        msg = f"Condition '{user.condition}' not recognized"
        raise ValueError(msg)


def session_creation(user):
    from learner.models.session import Session
    # last_session = \
    #     user.session_set.order_by("available_time").reverse().first()
    # print("user condition", user.condition)

    if user.condition == Condition.TEST:

        # if last_session is None:
        #     available_time = timezone.now()
        # else:

        # available_time = \
        #     last_session.available_time + datetime.timedelta(minutes=5)

        obj = Session.objects.create(
            user=user,
            available_time=timezone.now(),
            next_available_time=timezone.now() + datetime.timedelta(minutes=0),
            n_iteration=15,
            mcts=user.mctsteacher,
            # threshold=user.threshold,
            # leitner=user.leitner,
        )

        return obj

    else:
        msg = f"condition '{user.condition}' not recognized"
        raise ValueError(msg)
