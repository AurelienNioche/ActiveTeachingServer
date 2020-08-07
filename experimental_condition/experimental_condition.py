from django.utils import timezone
import datetime


class Condition:
    LEITNER = 0
    EXP_DECAY_THR_GRID = 1
    WALSH_THR_GRID = 2
    EXP_DECAY_SAMP_GRID = 3
    WALSH_SAMP_GRID = 4
    # MCTS = 3
    # THRESHOLD_ITEM_SPECIFIC = 4
    # MCTS_ITEM_SPECIFIC = 5


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
    walsh_bounds = (
        (0.8, 1.2),
        (0.03, 0.05),
        (0.005, 0.20),
        (0.005, 0.20),
        (0.1, 0.1),
        (0.6, 0.6))

    exp_decay_grid_size = 20
    walsh_grid_size = 10

    time_per_iter = 2

    sampling_iter_limit = 500
    sampling_horizon = 15

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

    elif user.condition == Condition.EXP_DECAY_THR_GRID:
        is_item_specific = False

        threshold = Threshold.objects.create(
            user=user,
            n_item=n_item,
            learnt_threshold=learnt_threshold)

        psy = Psychologist.objects.create(
            user=user,
            n_item=n_item,
            is_item_specific=is_item_specific,
            grid_size=exp_decay_grid_size,
            bounds=exp_decay_bounds)

        learner = ExpDecay.objects.create(
            n_item=n_item,
            user=user)

        TeachingEngine.objects.create(
            user=user,
            material=material,
            threshold=threshold,
            psychologist=psy,
            exp_decay=learner)

    elif user.condition == Condition.WALSH_THR_GRID:

        is_item_specific = False

        threshold = Threshold.objects.create(
            user=user,
            n_item=n_item,
            learnt_threshold=learnt_threshold)

        psy = Psychologist.objects.create(
            user=user,
            n_item=n_item,
            is_item_specific=is_item_specific,
            grid_size=walsh_grid_size,
            bounds=walsh_bounds)

        learner = Walsh2018.objects.create(
            n_item=n_item,
            user=user)

        TeachingEngine.objects.create(
            user=user,
            material=material,
            threshold=threshold,
            psychologist=psy,
            walsh=learner)

    elif user.condition == Condition.EXP_DECAY_SAMP_GRID:

        is_item_specific = False

        sampling = Sampling.objects.create(
            user=user,
            n_item=n_item,
            learnt_threshold=learnt_threshold,
            iter_limit=sampling_iter_limit,
            horizon=sampling_horizon,
            time_per_iter=time_per_iter)

        psy = Psychologist.objects.create(
            user=user,
            n_item=n_item,
            is_item_specific=is_item_specific,
            grid_size=exp_decay_grid_size,
            bounds=exp_decay_bounds)

        exp_decay = ExpDecay.objects.create(
            n_item=n_item,
            user=user)

        TeachingEngine.objects.create(
            user=user,
            material=material,
            sampling=sampling,
            psychologist=psy,
            exp_decay=exp_decay)

    elif user.condition == Condition.WALSH_SAMP_GRID:

        is_item_specific = False

        sampling = Sampling.objects.create(
            user=user,
            n_item=n_item,
            learnt_threshold=learnt_threshold,
            iter_limit=sampling_iter_limit,
            horizon=sampling_horizon,
            time_per_iter=time_per_iter)

        psy = Psychologist.objects.create(
            user=user,
            n_item=n_item,
            is_item_specific=is_item_specific,
            grid_size=walsh_grid_size,
            bounds=walsh_bounds)

        walsh = Walsh2018.objects.create(
            n_item=n_item,
            user=user)

        TeachingEngine.objects.create(
            user=user,
            material=material,
            sampling=sampling,
            psychologist=psy,
            walsh=walsh)

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

        # if last_session is None:
        #     available_time = timezone.now()
        # else:

        # available_time = \
        #     last_session.available_time + datetime.timedelta(minutes=5)

    if user.condition == Condition.LEITNER:
        te = user.teachingengine_set.exclude(leitner=None).first()

    elif user.condition == Condition.EXP_DECAY_THR_GRID:
        te = user.teachingengine_set.exclude(exp_decay=None,
                                             threshold=None,
                                             psychologist=None).first()

    elif user.condition == Condition.WALSH_THR_GRID:
        te = user.teachingengine_set.exclude(walsh=None,
                                             threshold=None,
                                             psychologist=None).first()

    elif user.condition == Condition.EXP_DECAY_SAMP_GRID:
        te = user.teachingengine_set.exclude(exp_decay=None,
                                             sampling=None,
                                             psychologist=None).first()

    elif user.condition == Condition.WALSH_SAMP_GRID:
        te = user.teachingengine_set.exclude(walsh=None,
                                             sampling=None,
                                             psychologist=None).first()

    else:
        msg = f"condition '{user.condition}' not recognized"
        raise ValueError(msg)

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
        teaching_engine=te)

    return obj

