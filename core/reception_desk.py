import numpy as np
from datetime import datetime
from types import SimpleNamespace

from learner.models import Question, User
from teaching_material.models import Meaning, Kanji

from core.task_parameters import N_POSSIBLE_REPLIES
from teaching_material.selection import JapaneseMaterial
import learner.authentication


USER_DEFAULT_ID = -1
USER_TEST_ID = -2

N_ITERATION = 150


class Subject:

    LOGIN = "login"
    SIGN_UP = "sign_up"
    QUESTION = "question"

    # def __init__(self, subject,
    #              msg=None,
    #              ok=None,
    #              n_iteration=None, user_id=None,
    #              t=-1,
    #              email=None,
    #              password=None,
    #              question=None,
    #              possible_replies=None,
    #              id_question=None,
    #              id_user_reply=None,
    #              is_new_question=None,
    #              id_correct_reply=None,
    #              success=None,
    #              time_display=None,
    #              time_reply=None,
    #              gender=None,
    #              mother_tongue=None,
    #              other_language=None,
    #              id_possible_replies=None):
    #
    #     self.subject = subject
    #     self.ok = ok
    #     self.msg = msg
    #
    #     self.n_iteration = n_iteration
    #     self.user_id = user_id
    #     self.t = t
    #
    #     self.id_user_reply = id_user_reply
    #     self.id_question = id_question
    #     self.id_possible_replies = id_possible_replies
    #     self.id_correct_reply = id_correct_reply
    #
    #     self.is_new_question = is_new_question
    #
    #     self.question = question
    #     self.possible_replies = possible_replies
    #
    #     self.success = success
    #     self.time_display = time_display
    #     self.time_reply = time_reply
    #
    #     self.email = email
    #     self.password = password
    #     self.gender = gender
    #     self.mother_tongue = mother_tongue
    #     self.other_language = other_language


def set_question(question_obj):
    r = SimpleNamespace()
    r.id_question = question_obj.question.id
    r.id_possible_replies = \
        [p.id for p in question_obj.possible_replies.all()]
    r.id_correct_reply = question_obj.question.meaning.id
    r.question = question_obj.question.kanji
    r.possible_replies = \
        [p.meaning for p in question_obj.possible_replies.all()]
    r.is_new_question = question_obj.new
    r.n_iteration = N_ITERATION
    r.t = question_obj.t
    return r


def to_json_serializable_dic(obj):

    dic = obj.__dict__
    for (k, v) in dic.items():
        if type(v) == np.ndarray:
            dic[k] = [int(i) for i in v]
        elif type(v) == np.int64:
            dic[k] = int(v)

    return dic


def treat_request(r):
    r = SimpleNamespace(**r)
    # if r.subject == Subject.SIGN_UP:
    #
    #     user = learner.authentication.sign_up(r=r)
    #     if user is None:
    #         r.msg = "User already exists!"

    if r.subject == Subject.LOGIN:
        user = learner.authentication.login(email=r.email, password=r.password)
        if user is not None:
            return {"ok": True, "user_id": user.id}
        else:
            return {"ok": False}

    elif r.subject == Subject.QUESTION:

        user = User.objects.get(id=r.user_id)
        if user is None:
            raise ValueError(f"User not recognized (id={r.id})")
        register_user_reply(user=user, t=r.t, id_user_reply=r.id_user_reply,
                            time_display=r.time_display,
                            time_reply=r.time_reply,
                            success=r.success)

        hist_question = get_historic(user=user)
        t = len(hist_question)

        # Check for t_max
        if t == N_ITERATION:
            return {"t": -1}  # End of the session

        question = get_question_not_answered(user)

        if question is None:
            question = new_question(
                user=user,
                hist_question=hist_question)

        resp = set_question(question)
        return to_json_serializable_dic(resp)

    else:
        raise ValueError(
            f"Subject of the request not recognized: '{r.subject}'")


def new_question(user, hist_question):

    if hist_question.count():
        last_was_success = hist_question.reverse()[0].success
    else:
        last_was_success = False

    question = user.leitner.ask(last_was_success=last_was_success)

    possible_replies = get_possible_replies(user=user, question=question)

    question_entry = Question.objects.create(
        user=user,
        t=hist_question.count(),
        question=question,
        new=question not in [q.question for q in hist_question],
        possible_replies=possible_replies)

    return question_entry


def get_possible_replies(user, question):

    """
    Select randomly possible replies, including the correct one
    """

    id_replies = [q.meaning.id for q in user.leitner.material.all()]
    id_correct_reply = question.meaning.id
    hist_id_reply = [q.user_reply.id for q in user.question_set.all()]

    for i in hist_id_reply:
        assert i in id_replies, i

    all_seen_replies = list(np.unique(hist_id_reply))

    if id_correct_reply in all_seen_replies:
        all_seen_replies.remove(id_correct_reply)

    missing = N_POSSIBLE_REPLIES - (len(all_seen_replies) + 1)

    if missing <= 0:
        set_replies = all_seen_replies

    else:
        all_replies = list(np.unique(id_replies))
        for i in all_seen_replies:
            all_replies.remove(i)

        if id_correct_reply in all_replies:
            all_replies.remove(id_correct_reply)

        set_replies = \
            list(np.random.choice(all_replies, size=missing, replace=False)) \
            + all_seen_replies

    id_possible_replies = \
        [id_correct_reply, ] + list(np.random.choice(
            set_replies,
            size=N_POSSIBLE_REPLIES-1, replace=False))
    id_possible_replies = np.array(id_possible_replies)
    np.random.shuffle(id_possible_replies)

    return [Meaning.objects.get(id=i) for i in id_possible_replies]


def get_historic(user):

    # Get historic
    return user.question_set.exclude(user_reply=None).order_by('t')


def get_question_not_answered(user):

    entries_not_answered = user.question_set.filter(user_reply=None)
    if entries_not_answered:
        return entries_not_answered[0]
    else:
        return None


def register_user_reply(user, t, id_user_reply,
                        time_display,
                        time_reply,
                        success):

    if t >= 0:
        question = Question.objects.get(user=user, t=t)
        question.user_reply = Meaning.objects.get(id=id_user_reply)
        question.success = success
        question.time_display = convert_to_time(time_display)
        question.time_reply = convert_to_time(time_reply)
        question.save()


def convert_to_time(string_time):
    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')
