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

from experimental_condition.models.experiment \
    import ThresholdCondition, RecursiveCondition


def main():

    df = pd.read_csv(os.path.join("subscriptions", "active-teaching-data.csv"),
                     index_col=[0], sep=';')

    assert len(df["AnonName"].unique()) == len(df["AnonName"])

    conditions = {
        0: (RecursiveCondition.__name__, True),
        1: (RecursiveCondition.__name__, False),
        2: (ThresholdCondition.__name__, True),
        3: (ThresholdCondition.__name__, False)}

    cd_idx = 0

    begin_with_active = True

    for idx_row, row in df.iterrows():

        email = f"{row['AnonName']}@aalto.fi"
        if User.objects.filter(email=email).first() is None:

            day, month, year = row["StartDate"].split(".")
            hour, minute = row["SessionStartTime"].split(":")

            hour = f"{int(hour):02d}"
            minute = f"{int(minute):02d}"

            day = f"{int(day):02d}"
            month = f"{int(month):02d}"

            first_session_string = f"{year}-{month}-{day} {hour}:{minute}"
            first_session = datetime.datetime.fromisoformat(first_session_string)
            first_session = timezone("Europe/Helsinki").localize(first_session)
            first_session = first_session.astimezone(timezone('UTC'))

            password = str(row["Password"])
            cd, is_item_specific = conditions[cd_idx]

            user = sign_up(
                        email=email,
                        password=password,
                        condition=cd,
                        first_session=first_session,
                        begin_with_active=begin_with_active,
                        is_item_specific=is_item_specific)

            if user is not None:
                print(f"User '{email}' created with success! "
                      f"First session is: {first_session_string} "
                      f"Helsinki Time")
            else:
                raise ValueError("WARNING!!! Something went wrong!")

        else:
            print(f"I will skip the user '{email}', "
                  f"he/she is already existing!")

        cd_idx += 1

        cd_idx %= len(conditions)
        begin_with_active = not begin_with_active


if __name__ == "__main__":
    main()
