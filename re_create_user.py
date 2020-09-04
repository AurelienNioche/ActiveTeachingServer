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

    previous_email = "peacock@aalto.fi"
    password = "5433"

    previous_u = User.objects.filter(email=previous_email).first()
    condition = previous_u.condition

    new_time = timezone("Europe/Helsinki")\
        .localize(datetime.datetime.fromisoformat("2020-09-05 08:00"))\
        .astimezone(timezone('UTC'))

    is_item_specific = previous_u.psychologist_set.first().is_item_specific

    begin_with_active = \
        previous_u.session_set.order_by("available_time").first()\
        .teaching_engine.leitner is None

    intermediary_email = previous_email.replace("aalto", "replace2")
    user = sign_up(
        email=intermediary_email,
        password=password,
        condition=condition,
        first_session=new_time,
        begin_with_active=begin_with_active,
        is_item_specific=is_item_specific,
        previous_email=previous_email)

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")

    print("Renaming")
    User.objects.filter(email=previous_email).delete()

    user.email = previous_email
    user.save()
    print("Done")


if __name__ == "__main__":
    main()
