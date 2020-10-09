import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd
import numpy as np

from user.models.user import User
from user_xp_kiwi_create import CSV


def main():

    users_df = pd.read_csv(CSV, index_col=0)

    users = User.objects.filter(is_superuser=False).order_by("email")

    male = 0
    female = 0
    other = 0

    ages = []

    for u in users:

        if 'active' not in u.email:
            continue

        all_session = u.session_set

        n_session_done = all_session.exclude(open=True).count()

        idx = users_df.index[users_df['app_email'] == u.email][0]
        user_row = users_df.loc[idx]

        if n_session_done < 14:
            email = user_row["Email"]
            print("drop:", email)
        else:
            gender = user_row["Gender"]
            if gender == "F":
                female += 1
            elif gender == "M":
                male += 1
            elif gender == "O":
                other += 1

            age = user_row["Age"]
            ages.append(age)

    print("male", male, "female", female, "other", other)
    print("age", np.mean(age), np.std(age))


if __name__ == "__main__":

    main()
    print("Done!")
