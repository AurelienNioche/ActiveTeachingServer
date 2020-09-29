""" Send an email upon account creation """
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone

application = get_wsgi_application()

import numpy as np
import pandas as pd
import datetime
from smtplib import SMTP_SSL
from pytz import timezone

import ActiveTeachingServer.credentials as credentials

from experimental_condition.models.experiment.condition_threshold \
    import ThresholdCondition
from experimental_condition.models.experiment.condition_forward \
    import ForwardCondition
from user.authentication import sign_up
from user.models.user import User


MAIL_DOMAIN = "active.fi"
CSV = os.path.join("subscriptions", "20200924-active-teaching-data.csv")


def update_date_and_time_on_csv(users_df, idx, datetime_obj):

    t = datetime_obj

    start_date = f"{t.day}.{t.month}.{t.year}"
    session_time = f"{t.hour:02d}:{t.minute:02d}"

    users_df.loc[idx, "StartDate"] = start_date
    users_df.loc[idx, "SessionTime"] = session_time


def update_note_on_csv(users_df, idx, msg):
    users_df.loc[idx, "Notes"] = msg


def save_csv(users_df):

    users_df["app_pwd"] = [get_password(r) for _, r in users_df.iterrows()]
    users_df.to_csv(CSV)


def get_password(user_row):
    return str(int(user_row["app_pwd"])).rjust(4, "0")


def main():

    new_start_string = f"2020-09-30 00:00"
    new_start = datetime.datetime.fromisoformat(new_start_string)
    new_start = timezone("Europe/Helsinki").localize(new_start)

    users_df = pd.read_csv(CSV, index_col=0)

    for idx, user_row in users_df.iterrows():

        contact_email = user_row["Email"]
        app_email = user_row["app_email"]
        mail_domain = app_email.split("@")[-1]
        password = get_password(user_row)

        previous_u = User.objects.get(email=app_email)

        first_ss = previous_u.session_set.order_by("available_time").first()
        initial_time = \
            first_ss.available_time.astimezone(timezone("Europe/Helsinki"))

        if initial_time > new_start:
            update_date_and_time_on_csv(users_df=users_df,
                                        idx=idx, datetime_obj=initial_time)
            save_csv(users_df)
            print(f"Everything is fine for {contact_email}")
            continue

        print(f"Re creating user for {contact_email}...")

        print("new start:", new_start)
        print("initial time:", initial_time)

        new_time = initial_time.replace(year=new_start.year,
                                        month=new_start.month,
                                        day=new_start.day)

        print("new time:", new_time)

        first_session = new_time.astimezone(timezone("UTC"))

        condition = previous_u.condition
        experiment_name = previous_u.experiment_name

        is_item_specific = previous_u.psychologist_set.first().is_item_specific

        begin_with_active = \
            previous_u.session_set.order_by("available_time").first() \
            .teaching_engine.leitner is None

        intermediary_email = app_email.replace(mail_domain, "replace")

        int_user = User.objects.filter(email=intermediary_email).first()
        if int_user is not None:
            int_user.delete()

        user = sign_up(
            email=intermediary_email,
            password=password,
            condition=condition,
            first_session=first_session,
            begin_with_active=begin_with_active,
            is_item_specific=is_item_specific,
            previous_email=app_email,
            experiment_name=experiment_name)

        if user is not None:
            print("Temporary user created!")
        else:
            raise ValueError("Error! User already exist!")

        print("Renaming...")
        previous_u.email = app_email.replace(mail_domain, "before")
        previous_u.save()
        # previous_u.delete()

        user.email = app_email
        user.save()

        print("Updating CSV...")
        update_date_and_time_on_csv(users_df=users_df,
                                    idx=idx, datetime_obj=first_session)
        update_note_on_csv(users_df=users_df, idx=idx, msg='reset')
        save_csv(users_df)

        print("Done!")
        print()


if __name__ == "__main__":
    main()
