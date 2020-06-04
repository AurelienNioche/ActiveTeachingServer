import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from learner.authentication import sign_up
from learner.models import User


def main():

    user = sign_up(
        email="james.jones@gmail.com",
        password="1234",
        gender=User.MALE,
        age=33,
        mother_tongue="french",
        other_language="english",
        condition=User.Condition.TEST
    )

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
