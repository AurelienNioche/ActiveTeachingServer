import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import datetime
from pytz import timezone

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.experiment \
    import ThresholdCondition, RecursiveCondition


def main():

    print("WELCOME! This will help you to create a user!")

    while True:
        condition = input("condition (enter '0' for 'threshold' and '1' for 'recursive'):")
        if condition not in ('0', '1'):
            print("I did not get the answer! Try again!")
        else:
            break

    condition = RecursiveCondition.__name__ if int(condition) \
        else ThresholdCondition.__name__

    print(f"condition selected: {condition}")

    while True:
        begin_with_active = input(
            "teacher to begin with (enter '0' for 'leitner' and '1' for 'active'):")
        if begin_with_active not in ('0', '1'):
            print("I did not get the answer! Try again!")
        else:
            break

    begin_with_active = bool(int(begin_with_active))
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

    while True:
        gender = input("gender (enter '0' for female and '1' for male):")
        if gender not in ('0', '1'):
            print("I did not get the answer! Try again!")
        else:
            break

    gender = User.MALE if int(gender) else User.FEMALE

    while True:
        try:
            age = int(input("age:"))
            break
        except Exception:
            print("I did not get the answer! Try again!")

    mother_tongue = input("mother tongue:")
    other_language = input("other language(s) (please separate by ','):")

    while True:

        try:

            first_session_string = input("Helsinki time for the first session (enter using YYYY-MM-DD HH:MM format, ex: '2020-11-04 08:00'):")

            first_session = datetime.datetime.fromisoformat(first_session_string)
            first_session = timezone("Europe/Helsinki").localize(first_session)
            first_session = first_session.astimezone(timezone('UTC'))
            break

        except Exception as e:
            print(f"Got exception '{e}', please try again!")

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
        begin_with_active=begin_with_active)

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Something went wrong!")


if __name__ == "__main__":
    main()
