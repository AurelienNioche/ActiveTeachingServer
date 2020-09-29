from teaching.models.teacher.evaluator import Evaluator
from teaching.models.teaching_engine import TeachingEngine

from teaching.models.teacher.leitner import Leitner
from teaching.models.teacher.threshold import Threshold
from teaching.models.teacher.recursive import Recursive
from teaching.models.teacher.forward import Forward
from teaching.models.psychologist.bayesian_grid import Psychologist
from teaching.models.learner.exp_decay import ExpDecay

from config import config


def create_leitner_engine(user, material):

    leitner = Leitner.objects.create(
        user=user,
        n_item=config.N_ITEM,
        delay_factor=config.LEITNER_DELAY_FACTOR,
        delay_min=config.LEITNER_DELAY_MIN)

    ev = Evaluator.objects.create(
        user=user,
        n_item=config.N_ITEM,
        n_repetition=config.EVAL_N_REPETITION)

    return TeachingEngine.objects.create(
        user=user,
        material=material,
        leitner=leitner,
        evaluator=ev)


def create_exp_decay_recursive_engine(user, material,
                                      is_item_specific):

    exp_decay = ExpDecay.objects.create(
        n_item=config.N_ITEM,
        user=user)

    psy = Psychologist.objects.create(
        user=user,
        n_item=config.N_ITEM,
        is_item_specific=is_item_specific,
        grid_size=config.GRID_SIZE,
        grid_methods=config.GRID_METHODS,
        bounds=config.BOUNDS
    )

    ev = Evaluator.objects.create(
        user=user,
        n_item=config.N_ITEM,
        n_repetition=config.EVAL_N_REPETITION)

    recursive = Recursive.objects.create(
        user=user,
        n_item=config.N_ITEM,
        learnt_threshold=config.LEARNT_THRESHOLD,
        time_per_iter=config.TIME_PER_ITER,
        n_iter_per_session=config.N_ITER_PER_SESSION)

    return TeachingEngine.objects.create(
        user=user,
        material=material,
        evaluator=ev,
        exp_decay=exp_decay,
        recursive=recursive,
        psychologist=psy)


def create_exp_decay_forward_engine(user, material,
                                    is_item_specific):

    exp_decay = ExpDecay.objects.create(
        n_item=config.N_ITEM,
        user=user)

    psy = Psychologist.objects.create(
        user=user,
        n_item=config.N_ITEM,
        is_item_specific=is_item_specific,
        grid_size=config.GRID_SIZE,
        grid_methods=config.GRID_METHODS,
        bounds=config.BOUNDS
    )

    ev = Evaluator.objects.create(
        user=user,
        n_item=config.N_ITEM,
        n_repetition=config.EVAL_N_REPETITION)

    forward = Forward.objects.create(
        user=user,
        n_item=config.N_ITEM,
        learnt_threshold=config.LEARNT_THRESHOLD,
        time_per_iter=config.TIME_PER_ITER,
        n_iter_per_session=config.N_ITER_PER_SESSION)

    return TeachingEngine.objects.create(
        user=user,
        material=material,
        evaluator=ev,
        exp_decay=exp_decay,
        forward=forward,
        psychologist=psy)


def create_exp_decay_threshold_engine(user, material,
                                      is_item_specific):

    exp_decay = ExpDecay.objects.create(
        n_item=config.N_ITEM,
        user=user)

    psy = Psychologist.objects.create(
        user=user,
        n_item=config.N_ITEM,
        is_item_specific=is_item_specific,
        grid_size=config.GRID_SIZE,
        grid_methods=config.GRID_METHODS,
        bounds=config.BOUNDS)

    ev = Evaluator.objects.create(
        user=user,
        n_item=config.N_ITEM,
        n_repetition=config.EVAL_N_REPETITION)

    threshold = Threshold.objects.create(
        user=user,
        n_item=config.N_ITEM,
        learnt_threshold=config.LEARNT_THRESHOLD)

    return TeachingEngine.objects.create(
        user=user,
        material=material,
        evaluator=ev,
        exp_decay=exp_decay,
        threshold=threshold,
        psychologist=psy)
