import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
application = get_wsgi_application()

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.experiment import Experiment


def main():

    email = "xp@test.com"
    condition = Experiment.__name__

    User.objects.filter(email=email).delete()

    user = sign_up(
        email=email,
        password="1234",
        gender=User.MALE,
        age=33,
        mother_tongue="french",
        other_language="english",
        condition=condition,
        first_session=timezone.now()
    )

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
