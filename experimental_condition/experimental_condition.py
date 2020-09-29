from experimental_condition.models.test_leitner import TestLeitner
from experimental_condition.models.pilot import Pilot
from experimental_condition.models.experiment.condition_forward import ForwardCondition
from experimental_condition.models.experiment.condition_threshold import ThresholdCondition
from experimental_condition.models.experiment.condition_recursive import RecursiveCondition
from experimental_condition.models.test_active import TestActive

CONDITION = {cls.__name__: cls for cls in (
    TestLeitner, Pilot, TestActive,
    ThresholdCondition, RecursiveCondition, ForwardCondition
)}


def user_creation(user, *args, **kwargs):

    CONDITION[user.condition].objects.create(user=user, *args, **kwargs)


def session_creation(user):

    return CONDITION[user.condition].objects.get(user=user).new_session()
