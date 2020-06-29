from django.utils import timezone
import datetime

class Condition:
    LEITNER = 0
    THRESHOLD = 1
    MCTS = 2
    THRESHOLD_ITEM_SPECIFIC = 1
    MCTS_ITEM_SPECIFIC = 1


def user_creation(user):

    from teacher.models.leitner import Leitner
    from teacher.models.threshold import Threshold
    from teacher.models.mcts import MCTSTeacher
    from teaching_material.models import Kanji

    material = Kanji.objects.all()[0:50]

    learnt_threshold = 0.90
    bounds = ((0.001, 0.04), (0.2, 0.5))
    grid_size = 20

    mcts_horizon = 10
    mcts_time_limit = None

    leitner_delay_factor = 2
    leitner_delay_min = 2

    if user.condition == Condition.LEITNER:

        Leitner.objects.create(user=user,
                               material=material,
                               delay_factor=leitner_delay_factor,
                               delay_min=leitner_delay_min)

    elif user.condition == Condition.THRESHOLD:
        is_item_specific = False
        Threshold.objects.create(user=user,
                                 material=material,
                                 learnt_threshold=learnt_threshold,
                                 is_item_specific=is_item_specific,
                                 bounds=bounds,
                                 grid_size=grid_size)
    elif user.condition == Condition.THRESHOLD_ITEM_SPECIFIC:
        is_item_specific = True
        Threshold.objects.create(user=user,
                                 material=material,
                                 learnt_threshold=learnt_threshold,
                                 is_item_specific=is_item_specific,
                                 bounds=bounds,
                                 grid_size=grid_size)

    elif user.condition == Condition.MCTS:
        is_item_specific = False
        MCTSTeacher.objects.create(user=user,
                                   material=material,
                                   learnt_threshold=learnt_threshold,
                                   bounds=bounds,
                                   grid_size=grid_size,
                                   is_item_specific=is_item_specific,
                                   iter_limit=500,
                                   time_limit=mcts_time_limit,
                                   horizon=mcts_horizon,
                                   time_per_iter=2)

    elif user.condition == Condition.MCTS_ITEM_SPECIFIC:
        is_item_specific = True
        MCTSTeacher.objects.create(user=user,
                                   material=material,
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

    if user.condition in (Condition.LEITNER, Condition.THRESHOLD,
                          Condition.THRESHOLD_ITEM_SPECIFIC,
                          Condition.MCTS_ITEM_SPECIFIC,
                          Condition.MCTS):

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
        )

        if user.condition == Condition.LEITNER:
            obj.leitner = user.leitner
        elif user.condition in (Condition.THRESHOLD, Condition.THRESHOLD_ITEM_SPECIFIC):
            obj.threshold = user.threshold
        else:
            obj.mcts = user.mctsteacher
        obj.save()
        return obj

    else:
        msg = f"condition '{user.condition}' not recognized"
        raise ValueError(msg)
