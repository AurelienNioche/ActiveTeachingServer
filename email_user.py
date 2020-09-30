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

from experimental_condition.models.experiment.condition_threshold import ThresholdCondition
from experimental_condition.models.experiment.condition_forward import ForwardCondition

from user.authentication import sign_up
from user.models.user import User


from user_xp_kiwi_create import main_email, CSV
from user_xp_kiwi_postpone import get_password


def main(experiment_name="kiwi", is_item_specific=True):

    contact_email = input("Contact email:")

    users_df = pd.read_csv(CSV, index_col=0)

    idx = users_df.index[users_df['Email'] == contact_email][0]
    user_row = users_df.loc[idx]

    app_email = user_row["app_email"]
    contact_email = user_row["Email"]
    start_date = user_row["StartDate"]
    session_time = user_row["SessionTime"]
    app_pwd = get_password(user_row)


    print("Mailing user...")
    main_email(contact_email=contact_email,
               app_email=app_email,
               app_pwd=app_pwd,
               date=start_date,
               time=session_time)


if __name__ == "__main__":
    main()
