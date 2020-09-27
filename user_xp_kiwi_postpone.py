import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import datetime
import argparse

import pandas as pd

from user.authentication import sign_up
from user.models.user import User

from user_xp_kiwi_create import set_first_session


MAIL_DOMAIN = "active.fi"
CSV = os.path.join("subscriptions", "20200924-active-teaching-data.csv")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("quantity", help="how long", type=int)
    parser.add_argument("-D", "--day", help="use days", action="store_true")
    parser.add_argument("-H", "--hour", help="use hours", action="store_true")
    args = parser.parse_args()
    if args.day:
        change = datetime.timedelta(days=args.quantity)
        change_str = f"{args.quantity} day"
        print(f"Change is {change_str}")
    elif args.hour:
        change = datetime.timedelta(hours=args.quantity)
        change_str = f"{args.quantity} hour"
        print(f"Change is {change_str}")

    else:
        raise ValueError

    users_df = pd.read_csv(CSV, index_col=0)

    contact_email = input("Contact email:")

    idx = users_df.index[users_df['Email'] == contact_email][0]
    user_row = users_df.loc[idx]

    answer = input(f"Proceed for {user_row['Email']}? ('y' to continue)")
    if answer in ('y', 'yes'):
        print("Proceed...")
    else:
        print("Operation cancelled")
        exit(0)

    previous_email = user_row["app_email"]
    mail_domain = previous_email.split("@")[-1]
    password = str(user_row["app_pwd"])
    start_date = user_row["StartDate"]
    session_time = user_row["SessionTime"]
    first_session = set_first_session(start_date=start_date,
                                      session_time=session_time)
    first_session += change

    msg = f"Actually began {change_str} later"
    if isinstance(user_row["Notes"], str) and user_row["Notes"] != "":
        new_note = f"{user_row['Notes']}\n{msg}"
    else:
        new_note = msg

    users_df.loc[idx, "Notes"] = new_note

    previous_u = User.objects.get(email=previous_email)

    print("Re creating user...")

    condition = previous_u.condition
    experiment_name = previous_u.experiment_name

    is_item_specific = previous_u.psychologist_set.first().is_item_specific

    begin_with_active = \
        previous_u.session_set.order_by("available_time").first()\
        .teaching_engine.leitner is None

    intermediary_email = previous_email.replace(mail_domain, "replace")
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
        print("Temporary user created!")
    else:
        raise ValueError("Error! User already exist!")

    print("Renaming...")
    User.objects.filter(email=previous_email).delete()

    user.email = previous_email
    user.save()

    print("Updating csv...")
    users_df.to_csv(CSV)
    print("Done!")


if __name__ == "__main__":
    main()
