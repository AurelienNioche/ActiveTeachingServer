from django.utils import timezone

class Condition:
    TEST = 0


def user_creation(user):

    from teacher.models.leitner import Leitner
    from teacher.models.threshold import Threshold
    from teaching_material.models import Kanji

    if user.condition == Condition.TEST:

        material = Kanji.objects.all()
        Leitner.objects.create(user=user,
                               material=material[0:50],
                               delay_factor=2)
        Threshold.objects.create(user=user,
                                 material=material[50:100],
                                 learnt_threshold=0.90,
                                 heterogeneous_param=True,
                                 bounds=((0.001, 0.04), (0.2, 0.5)),
                                 grid_size=20)

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
            n_iteration=10,
            threshold=user.threshold,
            # leitner=user.leitner,
        )

        return obj

    else:
        msg = f"condition '{user.condition}' not recognized"
        raise ValueError(msg)
