import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd
import numpy as np
from pytz import timezone

from user.models.user import User


def get_n_eval_n_recall(teaching_engine):
    if teaching_engine.evaluator.eval_done:
        ss = teaching_engine.session_set.filter(is_evaluation=True).first()
        q = ss.question_set.order_by("time_display")
        q_id = np.array(q.values_list("item_id", flat=True))
        q_r = np.array(q.values_list("success", flat=True))
        u_id = np.unique(q_id)
        n_recall = np.sum([np.all(q_r[q_id == id_]) for id_ in u_id])
        n = len(u_id)
    else:
        n, n_recall = None, None
    return n, n_recall


def main():

    users = User.objects.filter(is_superuser=False).order_by("email")
    row_list = []
    for u in users:

        print("u", u.email)
        if 'active' not in u.email:
        # if 'test' in u.email or 'replace' in u.email or 'before' in u.email:
            print(f"ignore '{u.email}'")
            print()
            continue

        te_leitner = u.teachingengine_set.exclude(leitner=None).first()

        te_thr = u.teachingengine_set.exclude(threshold=None).first()
        te_recursive = u.teachingengine_set.exclude(recursive=None).first()
        te_forward = u.teachingengine_set.exclude(forward=None).first()

        if te_thr is not None:
            teacher_md = "threshold"
            te_active = te_thr
        elif te_recursive is not None:
            teacher_md = "recursive"
            te_active = te_recursive
        elif te_forward is not None:
            teacher_md = "forward"
            te_active = te_forward
        else:
            print("ignore")
            print()
            continue

        all_session = u.session_set.order_by("available_time")
        n_session_done = all_session.exclude(open=True).count()

        try:
            domain = u.email.split("@")[-1]
        except:
            domain = None

        u_psy = u.psychologist_set.first()
        is_item_specific = u_psy.is_item_specific
        param = u_psy.inferred_learner_param()
        id_items = te_active.id_items

        if is_item_specific:

            for i, id_i in enumerate(id_items):

                assert len(param[i]) == 2

                row_list.append({
                    "user": u.email,
                    "domain": domain,
                    "is_item_specific": is_item_specific,
                    "n_ss_done": n_session_done,
                    "item": id_i,
                    "alpha": param[i, 0],
                    "beta": param[i, 1]
                })

        else:
            row_list.append({
                "user": u.email,
                "domain": domain,
                "is_item_specific": is_item_specific,
                "n_ss_done": n_session_done,
                "item": None,
                "alpha": param[0],
                "beta": param[1]
            })

    df = pd.DataFrame(row_list)

    df.sort_values("n_ss_done", inplace=True, ascending=False)
    df.to_csv(os.path.join("data_psy_estimates.csv"))


if __name__ == "__main__":

    main()
    print("Done!")
