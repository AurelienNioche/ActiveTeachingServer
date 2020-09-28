import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd

from user.models.user import User
# from user.models.session import Session
# from user.models.question import Question

MAIL_DOMAIN = "active.fi"
CSV = os.path.join("subscriptions", "20200924-active-teaching-data.csv")


def get_password(user_row):
    return str(int(user_row["app_pwd"])).rjust(4, "0")


def main():

    users_df = pd.read_csv(CSV, index_col=0)

    # Correct the csv
    for idx, user_row in users_df.iterrows():

        actual_pwd = get_password(user_row)
        # users_df.loc[idx, "app_pwd"] = actual_pwd
        # users_df.to_csv(CSV)

        email = user_row["app_email"]
        u = User.objects.get(email=email)
        u.set_password(actual_pwd)
        u.save()

# for u in User.objects.exclude(is_superuser=True):
#     if 'test' not in u.email:
#         u.experiment_name = "2020-09-04"
#         u.save()


if __name__ == "__main__":
    main()
    print("Done!")
