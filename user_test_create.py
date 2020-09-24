import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.experiment \
    import RecursiveCondition, ThresholdCondition, ForwardCondition


def main():

    while True:
        binary_cd = input("condition "
                          "(enter '0' for 'threshold' and "
                          "'1' for 'forward'):")
        if binary_cd not in ('0', '1'):
            print("I did not get the answer! Try again!")
        else:
            break

    condition = ForwardCondition.__name__ if int(binary_cd) \
        else ThresholdCondition.__name__

    email = "fwd@test.com" if int(binary_cd) else "thr@test.com"

    r = input("Begin with active teacher? "
              "(enter 'yes' or 'y' for 'item specific' condition)?")

    begin_with_active = r in ('y', 'yes', '')


    # r = input("Item specific? "
    #           "(enter 'yes' or 'y' for 'item specific' condition)?")
    # is_item_specific = r in ('y', 'yes')

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
