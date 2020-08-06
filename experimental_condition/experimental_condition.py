from django.utils import timezone
import datetime

class Condition:
    LEITNER = 0
    THRESHOLD = 1
    MCTS = 2
    THRESHOLD_ITEM_SPECIFIC = 1
    MCTS_ITEM_SPECIFIC = 1


def user_creation(user):

    from teaching.models.teacher.leitner import Leitner
    from teaching.models.teacher.threshold import Threshold
    from teaching.models.teacher.mcts import MCTSTeacher
    from teaching.models.teacher.sampling import Sampling
    from teaching_material.models import Kanji
    from teaching.models.teaching_engine import TeachingEngine
    from teaching.models.psychologist.bayesian_grid import Psychologist
    from teaching.models.learner.exp_decay import ExpDecay
    from teaching.models.learner.walsh import Walsh2018

    material = Kanji.objects.all()[0:50]

    learnt_threshold = 0.90

    exp_decay_bounds = ((0.001, 0.04), (0.2, 0.5))

    grid_size = 20

    mcts_horizon = 10
    mcts_time_limit = None

    leitner_delay_factor = 2
    leitner_delay_min = 2

    n_item = material.count()

    if user.condition == Condition.LEITNER:

        leitner = Leitner.objects.create(
            user=user,
            n_item=material.count(),
            delay_factor=leitner_delay_factor,
            delay_min=leitner_delay_min)
        TeachingEngine.objects.create(
            user=user,
            material=material,
            leitner=leitner)

    elif user.condition == Condition.THRESHOLD:
        is_item_specific = False

        threshold = Threshold.objects.create(
            user=user,
            n_item=n_item,
            learnt_threshold=learnt_threshold)

        psy = Psychologist.objects.create(
            user=user,
            n_item=n_item,
            is_item_specific=is_item_specific,
            grid_size=grid_size,
            bounds=exp_decay_bounds
        )

        learner = ExpDecay.objects.create(
            n_item=n_item,
            user=user
        )

        TeachingEngine.objects.create(
            user=user,
            material=material,
            threshold=threshold,
            psychologist=psy,
            exp_decay=learner
        )

    # elif user.condition == Condition.THRESHOLD_ITEM_SPECIFIC:
    #     is_item_specific = True
    #     Threshold.objects.create(user=user,
    #                              material=material,
    #                              learnt_threshold=learnt_threshold,
    #                              is_item_specific=is_item_specific,
    #                              bounds=bounds,
    #                              grid_size=grid_size)
    #
    # elif user.condition == Condition.MCTS:
    #     is_item_specific = False
    #     MCTSTeacher.objects.create(user=user,
    #                                material=material,
    #                                learnt_threshold=learnt_threshold,
    #                                bounds=bounds,
    #                                grid_size=grid_size,
    #                                is_item_specific=is_item_specific,
    #                                iter_limit=500,
    #                                time_limit=mcts_time_limit,
    #                                horizon=mcts_horizon,
    #                                time_per_iter=2)
    #
    # elif user.condition == Condition.MCTS_ITEM_SPECIFIC:
    #     is_item_specific = True
    #     MCTSTeacher.objects.create(user=user,
    #                                material=material,
    #                                learnt_threshold=learnt_threshold,
    #                                bounds=bounds,
    #                                grid_size=grid_size,
    #                                is_item_specific=is_item_specific,
    #                                iter_limit=500,
    #                                time_limit=None,
    #                                horizon=10,
    #                                time_per_iter=2)

    else:
        msg = f"Condition '{user.condition}' not recognized"
        raise ValueError(msg)


def session_creation(user):
    from experimental_condition.models.session import Session
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

        if user.condition == Condition.LEITNER:
            te = user.teachingengine_set.exclude(leitner=None).first()

        elif user.condition == Condition.THRESHOLD:
            te = user.teachingengine_set.exclude(exp_decay=None,
                                                 threshold=None,
                                                 psychologist=None).first()
        else:
            raise Exception

        # elif user.condition in (Condition.THRESHOLD,
        #                         Condition.THRESHOLD_ITEM_SPECIFIC):
        #     obj.threshold = user.threshold
        #
        # else:
        #     obj.mcts = user.mctsteacher
        obj = Session.objects.create(
            user=user,
            available_time=timezone.now(),
            next_available_time=timezone.now() + datetime.timedelta(minutes=0),
            n_iteration=15,
            teaching_engine=te
        )
        return obj

    else:
        msg = f"condition '{user.condition}' not recognized"
        raise ValueError(msg)
