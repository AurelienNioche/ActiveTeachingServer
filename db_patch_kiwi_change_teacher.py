""" Send an email upon account creation """
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import pandas as pd

from experimental_condition.models.experiment.condition_threshold \
    import ThresholdCondition
from experimental_condition.models.experiment.condition_forward \
    import ForwardCondition
from experimental_condition.models.experiment.condition_recursive \
    import RecursiveCondition
from user.authentication import sign_up
from user.models.user import User


MAIL_DOMAIN = "active.fi"
CSV = os.path.join("subscriptions", "20200924-active-teaching-data.csv")


def update_condition(users_df, idx, condition):

    users_df.loc[idx, "condition"] = start_date
    users_df.loc[idx, "SessionTime"] = session_time


def save_csv(users_df):

    users_df["app_pwd"] = [get_password(r) for _, r in users_df.iterrows()]
    users_df.to_csv(CSV)


def get_password(user_row):
    return str(int(user_row["app_pwd"])).rjust(4, "0")


def main():

    users_df = pd.read_csv(CSV, index_col=0)

    for idx, user_row in users_df.iterrows():

        contact_email = user_row["Email"]
        app_email = user_row["app_email"]
        mail_domain = app_email.split("@")[-1]
        password = get_password(user_row)

        previous_u = User.objects.get(email=app_email)
        old_condition = previous_u.condition

        if old_condition == ThresholdCondition.__name__:
            print(f"user '{contact_email}' is condition: '{old_condition}', I will ignore it\n")
            continue

        print(
            f"user '{contact_email}' is condition: '{old_condition}', I will modify it\n")
        assert old_condition == ForwardCondition.__name__

        new_condition = RecursiveCondition.__name__

        experiment_name = previous_u.experiment_name

        is_item_specific = previous_u.psychologist_set.first().is_item_specific

        begin_with_active = \
            previous_u.session_set.order_by("available_time").first() \
            .teaching_engine.leitner is None

        first_ss = previous_u.session_set.order_by("available_time").first()
        first_session = \
            first_ss.available_time

        intermediary_email = app_email.replace(mail_domain, "replace")

        int_user = User.objects.filter(email=intermediary_email).first()
        if int_user is not None:
            int_user.delete()

        user = sign_up(
            email=intermediary_email,
            password=password,
            condition=new_condition,
            first_session=first_session,
            begin_with_active=begin_with_active,
            is_item_specific=is_item_specific,
            previous_email=app_email,
            experiment_name=experiment_name)

        if user is not None:
            print("Temporary user created!")
        else:
            raise ValueError("Error! User already exist!")

        print("Deleting previous user")
        previous_u.delete()

        print("Renaming...")
        user.email = app_email
        user.save()

        print("Updating CSV...")
        update_condition(users_df=users_df,
                         idx=idx, condition=new_condition)
        save_csv(users_df)

        print("Done!")
        print()


if __name__ == "__main__":
    main()
