import numpy as np

from learner.models import Question, User
import learner.authentication


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
        available_session = user.session_set()

        return {"available": True}

    elif r["subject"] == Subject.QUESTION:

        user = User.objects.get(id=r["user_id"])
        question = Question.objects.get(r["question_id"])
        question.register_user_reply(
            user=user,
            id_user_reply=r["id_user_reply"],
            time_display=r["time_display"],
            time_reply=r["time_reply"],
            success=r["success"])

        q = Question.next_question(user, previous_question=question)
        if q is None:
            return {"session_done": -1}  # End of the session
        else:
            return {
                "question_id": q.question.id,
                "id_possible_replies": [p.id for p in q.possible_replies.all()],
                "id_correct_reply": q.question.meaning.id,
                "question": q.question.kanji,
                "possible_replies": [p.meaning for p in q.possible_replies.all()],
                "is_new_question": q.new,
                "n_iteration": q.session.n_iteration,
                "iter": q.session.iter
            }

    else:
        raise ValueError(
            f"Subject of the request not recognized: '{r.subject}'")


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



