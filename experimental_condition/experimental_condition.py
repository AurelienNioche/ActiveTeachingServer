from experimental_condition.models.test_leitner import TestLeitner
from experimental_condition.models.pilot import Pilot

CONDITION = {cls.__name__: cls for cls in (
    TestLeitner, Pilot
)}


def user_creation(user):

    if user.condition == TestLeitner.__name__:
        TestLeitner.objects.create(user=user)

    elif user.condition == Pilot.__name__:
        Pilot.objects.create(user=user)

    else:
        msg = f"Condition '{user.condition}' not recognized"
        raise ValueError(msg)


def session_creation(user):

    return CONDITION[user.condition].objects.get(user=user).new_session()
