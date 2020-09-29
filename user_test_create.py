import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.experiment.condition_forward import ForwardCondition
from experimental_condition.models.experiment.condition_threshold import ThresholdCondition
from experimental_condition.models.experiment.condition_recursive import RecursiveCondition


def main():

    while True:
        string_cd = input("condition "
                          "(enter '0' for 'threshold' and "
                          "'1' for 'forward',"
                          "'2' for 'recursive'):")
        if string_cd not in ('0', '1', '2'):
            print("I did not get the answer! Try again!")
        else:
            break

    num_cd = int(string_cd)
    if num_cd == 0:
        condition = ThresholdCondition.__name__
        email = "thr@test.com"
    elif num_cd == 1:
        condition = ForwardCondition.__name__
        email = "fwd@test.com"
    elif num_cd == 2:
        condition = RecursiveCondition.__name__
        email = "rec@test.com"
    else:
        raise ValueError

    r = input("Begin with active teacher? "
              "(enter 'yes' or 'y' for 'item specific' condition)?")

    begin_with_active = r in ('y', 'yes', '')

    # # Uncomment this for item specific manipulation
    # r = input("Item specific? "
    #           "(enter 'yes' or 'y' for 'item specific' condition)?")
    # is_item_specific = r in ('y', 'yes')

    print("Creating user...\n")

    is_item_specific = True

    User.objects.filter(email=email).delete()

    password = "1234"

    user = sign_up(
        email=email,
        password=password,
        condition=condition,
        first_session=timezone.now(),
        begin_with_active=begin_with_active,
        is_item_specific=is_item_specific,
        experiment_name="test")

    if user is not None:
        print(f"User '{email}' created.")
        print(f"Password: '{password}'")
        print(f"Condition: '{condition}'")
        print(f"Is 'Item specific':", is_item_specific)
        print(f"Begin with active teacher:", begin_with_active)
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
