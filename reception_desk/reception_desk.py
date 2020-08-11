from django.utils import timezone

from user.models.user import User
from user.models.question import Question
from user.models.session import Session
from user.authentication import login


from utils.time import datetime_to_sting

from random import shuffle


class Subject:

    LOGIN = "login"
    QUESTION = "question"
    SESSION = "session"
    # SIGN_UP = "sign_up"


def treat_request(r):

    if r["subject"] == Subject.LOGIN:
        u = login(email=r["email"], password=r["password"])
        if u is not None:
            return {
                "subject": Subject.LOGIN,
                "ok": True, "user_id": u.id
            }
        else:
            return {
                "subject": Subject.LOGIN,
                "ok": False
            }

    elif r["subject"] == Subject.SESSION:

        u = User.objects.get(id=r["user_id"])
        session = Session.get_user_session(user=u)

        if session is None:
            return {
                "subject": Subject.SESSION,
                "end": True,
                "available": False
            }
        elif session.is_available():
            return {
                "subject": Subject.SESSION,
                "available": True
            }
        else:
            return {
                "subject": Subject.SESSION,
                "available": False,
                "available_time": datetime_to_sting(session.available_time)
            }

    elif r["subject"] == Subject.QUESTION:

        a = timezone.now()

        u = User.objects.get(id=r["user_id"])
        previous_q = Question.objects.filter(id=r["question_id"]).first()
        if previous_q is not None:
            previous_q.register_user_reply(
                id_user_reply=r["id_user_reply"],
                time_display=r["time_display"],
                time_reply=r["time_reply"],
                success=r["success"])

        q = Question.next_question(u, previous_question=previous_q)
        b = timezone.now()
        print(f"Time to generate the question {b-a}")
        if q is None:
            return {
                "subject": Subject.QUESTION,
                "session_done": True
            }  # End of the session
        else:
            pr = list(q.possible_replies.all())
            shuffle(pr)

            return {
                "subject": Subject.QUESTION,
                "question_id": q.id,
                "id_possible_replies": [p.id for p in pr],
                "id_correct_reply": q.item.meaning.id,
                "question": q.item.value,
                "possible_replies": [p.meaning for p in pr],
                "is_new_question": q.new,
                "n_iteration": q.session.n_iteration,
                "iter": q.session.iter
            }

    else:
        raise ValueError(
            f"Subject of the request not recognized: '{r['subject']}'")


# def to_json_serializable_dic(obj):
#
#     dic = obj.__dict__
#     for (k, v) in dic.items():
#         if type(v) == np.ndarray:
#             dic[k] = [int(i) for i in v]
#         elif type(v) == np.int64:
#             dic[k] = int(v)
#
#     return dic
