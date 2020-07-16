import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import pickle
import numpy as np

from user_data.models import User, Question
from teaching_material.selection import kanji, meaning


def main():

    session = "pilot_2019_09_02"

    expected_n_trial = 750

    data = {
        "kanji": kanji,
        "meaning": meaning,
        "user_data": []
    }

    users = User.objects.all().order_by('id')
    for i, u in enumerate(users):
        qs = Question.objects.filter(user_id=u.id).order_by("time_reply")

        if len(qs) != expected_n_trial:
            continue

        data["user_data"].append({
            "kanji": kanji,
            "meaning": meaning,
            "time_reply": np.array([q.time_reply for q in qs]),
            "time_display": np.array([q.time_display for q in qs]),
            "hist": np.array([q.question for q in qs]),
            "success": np.array([q.success for q in qs])
        })

    with open(os.path.join("data", f"data_{session}.p"), "wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    main()
