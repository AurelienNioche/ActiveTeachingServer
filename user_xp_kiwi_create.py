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

from experimental_condition.models.experiment \
    import ThresholdCondition, ForwardCondition
from user.authentication import sign_up
from user.models.user import User


def get_credentials() -> dict:
    """Get email username and password"""
    return {
        "host": credentials.EMAIL_HOST_USER,
        "passwrd": credentials.EMAIL_HOST_PASSWORD}


def make_email_addr(local_part: str, domain_name: str) -> str:
    """Make a email-like string"""
    return f"{local_part}@{domain_name}"


def make_pin(seed) -> str:
    """Give a 4-digit PIN"""
    np.random.seed(seed)
    return str(np.random.randint(0, 9999)).rjust(4, "0")


def set_first_session(start_date, session_time):

    day, month, year = start_date.split(".")
    hour, minute = session_time.split(":")

    hour = f"{int(hour):02d}"
    minute = f"{int(minute):02d}"

    day = f"{int(day):02d}"
    month = f"{int(month):02d}"

    first_session_string = f"{year}-{month}-{day} {hour}:{minute}"
    first_session = datetime.datetime.fromisoformat(first_session_string)
    first_session = timezone("Europe/Helsinki").localize(first_session)
    first_session = first_session.astimezone(timezone('UTC'))

    return first_session


def main_email(contact_email, app_email, app_pwd, date, time):

    # Working to send plain text email
    # If you check internet to make the html version, filter results by date
    email_credentials = get_credentials()
    address_from = email_credentials["host"]
    address_to = (contact_email,)

    text = f"""From: hello@hello.com
    To: hi@hi.com\n
    Subject: <Subject goes here>\n
    Dear participant,

    Your account has been created!
    You can connect to:

    http://activeteaching.research.comnet.aalto.fi/

    id: {app_email}
    pwd: {app_pwd}

    Your first session is on {date} at {time}.

    Training plan: 2 sessions per day, for 7 days.

    Don't hesitate to reach me if you have any questions or concerns!

    Good luck!

    Best,
    Aurelien


    --
    Aurelien Nioche, PhD

    Finnish Center for Artificial Intelligence (FCAI)
    Aalto University
    Department of Communications and Networking
    Computer Science Building - Office B235
    Konemiehentie 2
    02150 Espoo, Finland
    phone: (FI) +358 (0) 5 04 75 83 05, (FR) +33 (0) 6 86 55 02 55
    mail: nioche.aurelien@gmail.com
    """

    with SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(email_credentials["host"], email_credentials["passwrd"])
        s.sendmail(address_from, address_to, text)


def main(file_name="20200924-active-teaching-data.csv",
         experiment_name="kiwi",
         is_item_specific=True):

    # Squeeze = load as pd.Series instead of pd.Dataframe
    animals_series = pd.read_csv("animals.csv", squeeze=True)

    users_df = pd.read_csv(
        os.path.join("subscriptions", file_name),
        index_col=0)

    users_df.to_csv(os.path.join("subscriptions", "BKP_" + file_name))

    # Create new columns
    # for c in ("app_email", "app_pwd"):
    #     if c not in users_df.columns:
    #         users_df[c] = ""

    conditions = {
        # Condition name, begin with active
        0: (ForwardCondition.__name__, True),
        1: (ThresholdCondition.__name__, True),
        2: (ForwardCondition.__name__, False),
        3: (ThresholdCondition.__name__, False)
    }

    cd_idx = 0

    for idx, user_row in users_df.iterrows():

        app_email = user_row["app_email"] if "app_email" in user_row else None

        if app_email:
            assert User.objects.filter(email=app_email).first() is not None
            continue
        print(user_row)
        contact_email = user_row["Email"]
        start_date = user_row["StartDate"]
        session_time = user_row["SessionTime"]

        app_email = make_email_addr(animals_series[idx],  "active.fi")
        if User.objects.filter(email=app_email).first() is not None:
            print(f"I will ignore the user {contact_email}, "
                  f"it is already registered")
            continue

        app_pwd = make_pin(seed=idx)

        condition, begin_with_active = conditions[cd_idx]

        first_session = set_first_session(
            start_date=start_date,
            session_time=session_time)

        # Confirm creation
        # ready = input("create user (enter 'yes' or 'y' to continue)?")
        # if ready not in ("y", "yes"):
        #     print("Operation cancelled")
        #     exit(0)

        user = sign_up(
            email=app_email,
            password=app_pwd,
            experiment_name=experiment_name,
            condition=condition,
            first_session=first_session,
            begin_with_active=begin_with_active,
            is_item_specific=is_item_specific)

        if user is not None:
            print("Success!")
            print("Updating csv...")
            users_df.loc[idx, "app_email"] = app_email
            users_df.loc[idx, "app_pwd"] = app_pwd
            users_df.loc[idx, "app_pwd"] = app_pwd
            users_df.loc[idx, "condition"] = condition
            users_df.loc[idx, "begin_with_active"] = begin_with_active

            print("Mailing user...")
            main_email(contact_email=contact_email,
                       app_email=app_email,
                       app_pwd=app_pwd,
                       date=start_date,
                       time=session_time)

            users_df.to_csv(os.path.join("subscriptions", file_name))

        else:
            print(f"Something went wrong with user {contact_email}!")

        cd_idx += 1
        cd_idx %= len(conditions)


if __name__ == "__main__":
    main("test.csv")
