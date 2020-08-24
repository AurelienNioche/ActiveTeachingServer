import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import datetime

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.pilot import Pilot
# from experimental_condition.models.test_active import TestActive
# from experimental_condition.models.test_leitner import TestLeitner

from teaching.models.learner.walsh import Walsh2018
from teaching.models.learner.exp_decay import ExpDecay

LEARNER_MODELS = (Walsh2018.__name__, ExpDecay.__name__)


def main():

    condition = Pilot.__name__

    # input("condition (only current option is 'Pilot'):")
    # if condition not in (Pilot.__name__, ):
    #     raise ValueError("Condition not recognized")
    email = input("email:")

    if User.objects.filter(email=email).first():
        print("Warning! User already exists!")
        erase_user = input("erase existing user (enter 'yes' or 'y' to continue)?")
        if erase_user:
            User.objects.filter(email=email).first().delete()
            print("previous user erased")
            print(f"email:{email}")
        else:
            print("can not create user with same email. Operation canceled")
            exit(0)

    password = input("password:")

    learner_model = input(f"learner model ({' or '.join(LEARNER_MODELS)}):")

    gender = input("gender (enter '0' for female and '1' for male):")
    if gender not in ('0', '1'):
        raise ValueError

    gender = User.MALE if int(gender) else User.FEMALE

    age = int(input("age:"))

    mother_tongue = input("mother tongue:")
    other_language = input("other language(s) (please separate by ','):")

    first_session_string = input("Time UTC for the first session (enter using HH:MM format, ex: 08:00):")

    first_session = datetime.time.fromisoformat(first_session_string)
    second_session = first_session.replace(minute=first_session.minute+5)

    ready = input("create user (enter 'yes' or 'y' to continue)?")
    if ready not in ('y', 'yes'):
        print("Operation cancelled")
        exit(0)

    user = sign_up(
        email=email,
        password=password,
        gender=gender,
        age=age,
        mother_tongue=mother_tongue,
        other_language=other_language,
        condition=condition,
        first_session=first_session,
        second_session=second_session,
        learner_model=learner_model
    )

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
