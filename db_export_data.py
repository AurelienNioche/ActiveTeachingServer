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
    for u in users:

        qs = Question.objects.filter(user=u).order_by("time_display")
        for q in qs:

            te = q.session.teaching_engine
            if te.leitner is not None:
                teacher_md = "leitner"
            elif te.threshold is not None:
                teacher_md = "threshold"
            elif te.sampling is not None:
                teacher_md = "sampling"
            else:
                raise ValueError

            if te.exp_decay is not None:
                learner_md = "exp_decay"
            elif te.walsh is not None:
                learner_md = "walsh"
            else:
                raise ValueError

            row = {
                "user": u.email,
                "condition": u.condition,
                "item": q.item.id,
                "success": q.success,
                "teacher_md": teacher_md,
                "learner_md": learner_md,
                "psy_md": "grid",
                "session": q.session_id,
                "is_eval": q.session.is_evaluation,
                "ts_display": q.time_display,
                "ts_reply": q.time_reply
            }
            row_list.append(row)

    df = pd.DataFrame(row_list)
    df.to_csv(os.path.join("results.csv"))

if __name__ == "__main__":

    main()
    print("Done!")
