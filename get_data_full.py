import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pandas as pd

from user.models.user import User
from user.models.question import Question


def main():
    row_list = []

    users = User.objects.filter(is_superuser=False)
    i = -1
    for u in users:

        # if 'test' in u.email or 'replace' in u.email or 'before' in u.email:
        #     print("ignore")
        #     print()
        #     continue
        if 'test' in u.email or 'replace' in u.email or 'before' in u.email:
            print(f"ignore: {u.email}")
            continue
        else:
            i += 1
            print(f"user {i}: {u.email}")

        n_session_done = u.session_set.exclude(open=True).count()

        qs = Question.objects.filter(user=u).order_by("time_display")
        for q in qs:

            te = q.session.teaching_engine
            if te.leitner is not None:
                teacher_md = "leitner"
            elif te.threshold is not None:
                teacher_md = "threshold"
            elif te.recursive is not None:
                teacher_md = "recursive"
            elif te.sampling is not None:
                teacher_md = "sampling"
            elif te.forward is not None:
                teacher_md = "forward"
            else:
                raise ValueError

            if te.exp_decay is not None:
                learner_md = "exp_decay"
            elif te.walsh is not None:
                learner_md = "walsh"
            else:
                learner_md = None

            try:
                domain = u.email.split("@")[-1]
            except:
                domain = None

            row = {
                "user": u.email,
                "domain": domain,
                "condition": u.condition,
                "item": q.item.id,
                "item_character": q.item.value,
                "item_meaning": q.item.meaning.meaning,
                "success": q.success,
                "teacher_md": teacher_md,
                "learner_md": learner_md,
                "psy_md": "grid",
                "session": q.session_id,
                "is_eval": q.session.is_evaluation,
                "ts_display": q.time_display,
                "ts_reply": q.time_reply,
                "n_session_done": n_session_done
            }
            for resp_idx, meaning in enumerate(q.possible_replies.all()):
                row.update({f"pos_reply_{resp_idx}": meaning.meaning})
            row_list.append(row)

    df = pd.DataFrame(row_list)
    df.to_csv(os.path.join("data_full.csv"))


if __name__ == "__main__":

    main()
    print("Done!")
