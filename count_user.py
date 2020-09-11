import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd
from tqdm import tqdm
import numpy as np

from user.models.user import User
from user.models.question import Question


def main():

    users = User.objects.filter(is_superuser=False).order_by("email")
    user_list = []
    done = []
    for u in tqdm(users):

        print("u", u.email)

        if 'test' in u.email:
            print("ignore")
            continue

        eval_done = [te.evaluator.eval_done
                     for te in u.teachingengine_set.all()]

        is_done = np.all(eval_done)
        print("is done", is_done)
        done.append(is_done)
        user_list.append(u.email)
        print()

    df = pd.DataFrame({"user": user_list, "done": done})
    df.to_csv(os.path.join("is_done.csv"))


if __name__ == "__main__":

    main()
    print("Done!")
