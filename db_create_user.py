import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.pilot import Pilot
# from experimental_condition.models.test_active import TestActive
# from experimental_condition.models.test_leitner import TestLeitner


def main():

    condition = Pilot.__name__

    # input("condition (only current option is 'Pilot'):")
    # if condition not in (Pilot.__name__, ):
    #     raise ValueError("Condition not recognized")
    email = input("email:")

    if User.objects.filter(email=email).first():
        raise ValueError("User already exists!")

    password = input("password:")
    gender = input("gender (enter '0' for female and '1' for male):")
    if gender not in ('0', '1'):
        raise ValueError

    gender = User.MALE if int(gender) else User.FEMALE

    age = int(input("age:"))

    mother_tongue = input("mother tongue:")
    other_language = input("other language(s) (please separate by ','):")

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
        condition=condition)

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
