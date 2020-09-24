from experimental_condition.models.test_leitner import TestLeitner
from experimental_condition.models.pilot import Pilot
from experimental_condition.models.experiment import \
    ThresholdCondition, RecursiveCondition, ForwardCondition
from experimental_condition.models.test_active import TestActive

CONDITION = {cls.__name__: cls for cls in (
    TestLeitner, Pilot, TestActive,
    ThresholdCondition, RecursiveCondition, ForwardCondition
)}


def user_creation(user, *args, **kwargs):

    CONDITION[user.condition].objects.create(user=user, *args, **kwargs)


def session_creation(user):

    return CONDITION[user.condition].objects.get(user=user).new_session()
