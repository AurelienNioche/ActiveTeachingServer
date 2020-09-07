import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import datetime
from pytz import timezone

from user.authentication import sign_up
from user.models.user import User


def main():
    while True:
        try:
            previous_email = input("previous_name:")
            previous_email = f"{previous_email}@aalto.fi"  #"name_to_replace@aalto.fi"
            previous_u = User.objects.get(email=previous_email)
            break
        except Exception as e:
            print(f"encountered error '{e}', please retry!")

    while True:
        try:
            new_time = input("new time (YYYY-MM-DD HH:MM):")
            new_time = timezone("Europe/Helsinki") \
                .localize(datetime.datetime.fromisoformat(new_time)) \
                .astimezone(timezone('UTC'))
            break

        except Exception as e:
            print(f"encountered error '{e}', please retry!")

    password = input("password:")

    print("Re creating user...")

    condition = previous_u.condition

    is_item_specific = previous_u.psychologist_set.first().is_item_specific

    begin_with_active = \
        previous_u.session_set.order_by("available_time").first()\
        .teaching_engine.leitner is None

    intermediary_email = previous_email.replace("aalto", "replace")
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
