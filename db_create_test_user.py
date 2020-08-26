import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.test_active import TestActive
# from experimental_condition.models.pilot import Pilot
# from experimental_condition.models.test_leitner import TestLeitner

from teaching.models.learner.walsh import Walsh2018
from teaching.models.learner.exp_decay import ExpDecay


def main():

    email = "active@test.com"
    condition = TestActive.__name__

    learner_model = Walsh2018.__name__   # "Walsh2018"

    exp_cst_time = 1 / (24 * 60**2)
    walsh_cst_time = 1 / (24 * 60**2)

    User.objects.filter(email=email).delete()

    user = sign_up(
        email=email,
        password="1234",
        gender=User.MALE,
        age=33,
        mother_tongue="french",
        other_language="english",
        condition=condition,
        learner_model=learner_model,
        exp_cst_time=exp_cst_time,
        walsh_cst_time=walsh_cst_time
    )

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
