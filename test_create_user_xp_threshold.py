import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
# from django.utils import timezone
application = get_wsgi_application()

import datetime
from pytz import timezone

from user.authentication import sign_up
from user.models.user import User

from experimental_condition.models.experiment import ThresholdCondition


def main():

    email = "peacock@aalto.fi"
    condition = ThresholdCondition.__name__

    # User.objects.filter(email=email).delete()

    user = sign_up(
        email="peacock2@aalto.fi",
        password="5433",
        condition=ThresholdCondition.__name__,
        first_session=timezone("Europe/Helsinki").localize(datetime.datetime.fromisoformat("2020-09-05 08:00")).astimezone(timezone('UTC')),
        begin_with_active=False,
        is_item_specific=False)

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")


if __name__ == "__main__":
    main()
