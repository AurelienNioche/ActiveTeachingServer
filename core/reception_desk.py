from learner.models.user import User
from learner.models.session import Session
from learner.models.question import Question
import learner.authentication

from utils.time import datetime_to_sting


class Subject:

    LOGIN = "login"
    QUESTION = "question"
    SESSION = "session"
    # SIGN_UP = "sign_up"


def treat_request(r):

    if r["subject"] == Subject.LOGIN:
        user = learner.authentication.login(email=r["email"],
                                            password=r["password"])
        if user is not None:
            return {"ok": True, "user_id": user.id}
        else:
            return {"ok": False}

    elif r["subject"] == Subject.SESSION:

        user = User.objects.get(id=r["user_id"])
        session = Session.get_user_session(user=user)

        if session is None:
            return {"end": True,
                    "available": False}
        elif session.is_available():
            return {"available": True}
        else:
            return {
                "available": False,
                "available_time": datetime_to_sting(session.available_time)}

    elif r["subject"] == Subject.QUESTION:

        user = User.objects.get(id=r["user_id"])
        previous_q = Question.objects.filter(id=r["question_id"]).first()
        if previous_q is not None:
            previous_q.register_user_reply(
                id_user_reply=r["id_user_reply"],
                time_display=r["time_display"],
                time_reply=r["time_reply"],
                success=r["success"])

        q = Question.next_question(user, previous_question=previous_q)
        if q is None:
            return {"session_done": -1}  # End of the session
        else:
            return {
                "question_id": q.id,
                "id_possible_replies": [p.id for p in q.possible_replies.all()],
                "id_correct_reply": q.item.meaning.id,
                "question": q.item.value,
                "possible_replies": [p.meaning for p in q.possible_replies.all()],
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
