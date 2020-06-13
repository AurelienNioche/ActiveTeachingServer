import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from learner.authentication import sign_up
from learner.models.user import User

from experimental_condition.experimental_condition import Condition


def main():
    email = "james.jones@gmail.com"
    User.objects.filter(email=email).delete()

    user = sign_up(
        email=email,
        password="1234",
        gender=User.MALE,
        age=33,
        mother_tongue="french",
        other_language="english",
        condition=Condition.TEST
    )

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
