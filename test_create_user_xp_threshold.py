import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.experiment import ThresholdCondition


def main():

    email = "thr@test.com"
    condition = ThresholdCondition.__name__

    User.objects.filter(email=email).delete()

    user = sign_up(
        email=email,
        password="1234",
        gender=User.MALE,
        age=33,
        mother_tongue="french",
        other_language="english",
        condition=condition,
        first_session=timezone.now(),
        begin_with_active=True)

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
