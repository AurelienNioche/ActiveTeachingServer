import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import datetime
from pytz import timezone

import pandas as pd

from user.authentication import sign_up
from user.models.user import User

from user_xp_kiwi_create import set_first_session


def main(file_name="20200924-active-teaching-data.csv"):

    users_df = pd.read_csv(
        os.path.join("subscriptions", file_name),
        index_col=0)

    while True:
        try:
            contact_email = input("contact email")

            idx = users_df.index[users_df['Email'] == contact_email].tolist()[0]
            user_row = users_df.iloc[idx]
            previous_email = user_row["app_email"]
            password = user_row["app_pwd"]
            start_date = user_row["StartDate"]
            session_time = user_row["SessionTime"]
            first_session = set_first_session(start_date=start_date,
                                              session_time=session_time)
            first_session += datetime.timedelta(days=1)
            previous_u = User.objects.get(email=previous_email)

            user_row["Notes"] += "Actually began 1 day later"

            break
        except Exception as e:
            print(f"encountered error '{e}', please retry!")

    print("Re creating user...")

    condition = previous_u.condition
    experiment_name = previous_u.experiment_name

    is_item_specific = previous_u.psychologist_set.first().is_item_specific

    begin_with_active = \
        previous_u.session_set.order_by("available_time").first()\
        .teaching_engine.leitner is None

    intermediary_email = previous_email.replace("aalto", "replace")
    user = sign_up(
        email=intermediary_email,
        password=password,
        condition=condition,
        first_session=first_session,
        begin_with_active=begin_with_active,
        is_item_specific=is_item_specific,
        previous_email=previous_email,
        experiment_name=experiment_name)

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Error! User already exist!")

    print("Renaming")
    User.objects.filter(email=previous_email).delete()

    user.email = previous_email
    user.save()

    print("Updating csv")
    users_df.to_csv(os.path.join("subscriptions", file_name))
    print("Done")


if __name__ == "__main__":
    main()
