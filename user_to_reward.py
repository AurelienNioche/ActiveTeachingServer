import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd

from user.models.user import User
from user_xp_kiwi_create import CSV


def main():

    users_df = pd.read_csv(CSV, index_col=0)

    users = User.objects.filter(is_superuser=False).order_by("email")
    for u in users:

        if 'active' not in u.email:
            continue

        all_session = u.session_set

        n_session_done = all_session.exclude(open=True).count()
        if n_session_done == 14:

            idx = users_df.index[users_df['app_email'] == u.email][0]
            user_row = users_df.loc[idx]
            print(user_row["Email"])


if __name__ == "__main__":

    main()
    print("Done!")
