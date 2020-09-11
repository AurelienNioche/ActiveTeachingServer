import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd
from tqdm import tqdm
import numpy as np
from pytz import timezone

from user.models.user import User
from user.models.question import Question


def main():

    users = User.objects.filter(is_superuser=False).order_by("email")
    row_list = []
    for u in users:

        print("u", u.email)

        if 'test' in u.email:
            print("ignore")
            print()
            continue

        te_leitner = u.teachingengine_set.exclude(leitner=None).first()

        te_thr = u.teachingengine_set.exclude(threshold=None).first()
        te_recursive = u.teachingengine_set.exclude(recursive=None).first()

        if te_thr is not None:
            teacher_md = "threshold"
            te_active = te_thr
        elif te_recursive is not None:
            teacher_md = "recursive"
            te_active = te_recursive
        else:
            print("ignore")
            print()
            continue

        is_item_specific = \
            u.psychologist_set.first().is_item_specific

        if te_leitner.evaluator.eval_done:
            ss = te_leitner.session_set.filter(is_evaluation=True).first()
            resp = ss.question_set.order_by("time_display").values_list(
                "success", flat=True)
            n_recall_leitner = np.sum(resp)
            n_eval_leitner = len(resp)
        else:
            n_recall_leitner, n_eval_leitner = None, None

        if te_active.evaluator.eval_done:
            ss = te_active.session_set.filter(is_evaluation=True).first()
            resp = ss.question_set.order_by("time_display").values_list(
                "success", flat=True)
            n_recall_act = np.sum(resp)
            n_eval_act = len(resp)
        else:
            n_recall_act, n_eval_act = None, None

        all_session = u.session_set.order_by("available_time")
        first_session = all_session.first()
        last_session = all_session.reverse().first()

        n_session_done = all_session.exclude(open=True).count()

        first_ss_av_time = \
            first_session.available_time.astimezone(
                timezone('Europe/Helsinki'))

        last_ss_av_time = \
            last_session.available_time.astimezone(
                timezone('Europe/Helsinki'))

        begin_with_active = all_session.first() \
            .teaching_engine.leitner is None

        row_list.append({
            "user": u.email,
            "teacher_md": teacher_md,
            "is_item_specific": is_item_specific,
            "begin_with_active": begin_with_active,
            "first_ss_av_time": first_ss_av_time,
            "last_ss_av_time": last_ss_av_time,
            "n_ss_done": n_session_done,
            "n_eval_leitner": n_eval_leitner,
            "n_recall_leitner": n_recall_leitner,
            "n_eval_act": n_eval_act,
            "n_recall_act": n_recall_act
        })

        # is_done = np.all(eval_done)
        # print("is done", is_done)
        # done.append(is_done)
        # user_list.append(u.email)
        # print()

    df = pd.DataFrame(row_list)

    df.sort_values("n_ss_done")
    df.to_csv(os.path.join("r.csv"))


if __name__ == "__main__":

    main()
    print("Done!")
