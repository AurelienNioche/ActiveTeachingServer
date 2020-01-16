import numpy as np
from datetime import datetime

from user.models import Question, User

from core.fixed_parameters import N_POSSIBLE_REPLIES
import teaching_material.selection
import user.authentication

from teacher.models import Leitner

from tools.utils import Atomic

USER_DEFAULT_ID = -1
USER_TEST_ID = -2


class Request:

    LOGIN = "login"
    SIGN_UP = "sign_up"

    def __init__(self, request_type=None, register_replies=None,
                 n_iteration=None, user_id=None, t=None, user_email=None,
                 user_password=None):

        self.type = request_type
        self.register_replies = register_replies
        self.n_iteration = n_iteration
        self.user_id = user_id
        self.t = t

        self.user_email = user_email
        self.user_password = user_password

    def return_to_user(self, question, possible_replies, id_question,
                       id_possible_replies, id_reply, is_new_question):
        return {
            'userId': int(self.user_id),
            't': int(self.t),
            'nIteration': int(self.n_iteration),
            'registerReplies': self.register_replies,
            'question': question,
            'possibleReplies': possible_replies,
            'idQuestion': int(id_question),
            'newQuestion': is_new_question,
            'idCorrectAnswer': int(id_reply),
            'idPossibleReplies': [int(i) for i in id_possible_replies],
        }


def treat_request(request_kwargs):

    r = Request(**request_kwargs)
    if r.type == Request.LOGIN:
        user.authentication.login(r)

    elif r.type == Request.SIGN_UP:
        user.authentication.sign_up(r)




    # teacher_name = reply['teacher']

    # first_call = reply['userId'] == USER_DEFAULT_ID

    # assert teacher_name == 'leitner', 'Only Leitner teacher is implemented!'

    # # Check for t_max
    # if t == t_max:
    #     return {
    #         't': -1
    #     }

    # if first_call:
    #     if register_replies:
    #         user_id = _register_user()
    #     else:
    #         user_id = USER_TEST_ID
    #     t = 0
    #
    # else:

    # TODO: redirect if sign up

    # TODO: redirect if login

    # TODO:  is the user is authorized to play?

    # TODO: which material should he use?

    # TODO: which teacher should he use?

    if r.register_replies:
        _register_question(r)
    r.t += 1

    id_questions, id_replies = teaching_material.selection.get_id()

    hist_question, hist_success = get_historic(user_id=r.user_id, t=r.t)

    if r.register_replies:
        id_question = \
            _new_question(
                user_id=r.user_id,
                t=r.t,
                hist_question=hist_question,
                hist_success=hist_success,
                id_questions=id_questions)

    else:
        id_question = \
            _random_question(id_questions=id_questions)

    id_reply = id_replies[id_question]

    id_possible_replies = \
        get_possible_replies(
            hist_question=hist_question,
            id_reply=id_reply,
            id_replies=id_replies
        )

    question, possible_replies = \
        teaching_material.selection.get_string_representation(
            id_question=id_question,
            id_possible_replies=id_possible_replies
        )

    is_new_question = id_question not in hist_question

    return reply.return_to_user(
        question=question, possible_replies=possible_replies,
        id_question=id_question, id_possible_replies=id_possible_replies,
        id_reply=id_reply, is_new_question=is_new_question)


def _convert_to_time(string_time):

    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')


def _random_question(id_questions):
    id_question = np.random.randint(len(id_questions))
    return id_question


def _new_question(user_id, t, id_questions,
                  hist_question, hist_success):

    if t == 0:
        # Create teacher
        teacher_id, teacher = _create_teacher(user_id=user_id,
                                              n_item=len(id_questions))
        question_id = teacher.ask(t=t, questions=id_questions)
        teacher.save()

    else:

        # Get teacher
        teacher = Leitner.objects.get(user_id=user_id)
        question_id = teacher.ask(
            t=t,
            hist_success=hist_success,
            hist_question=hist_question,
            questions=id_questions)
        teacher.save()

    return question_id


def get_possible_replies(id_replies, id_reply, hist_question):

    # Get hist of meanings
    hist_meaning = [id_replies[i] for i in hist_question]

    # Select randomly possible replies, including the correct one
    all_seen_replies = list(np.unique(hist_meaning))

    if id_reply in all_seen_replies:
        all_seen_replies.remove(id_reply)

    missing = N_POSSIBLE_REPLIES - (len(all_seen_replies) + 1)

    if missing <= 0:
        set_replies = all_seen_replies

    else:
        all_replies = list(np.unique(id_replies))
        for i in all_seen_replies:
            all_replies.remove(i)

        if id_reply in all_replies:
            all_replies.remove(id_reply)

        set_replies = \
            list(np.random.choice(all_replies, size=missing, replace=False)) \
            + all_seen_replies

    possible_replies = \
        [id_reply, ] + list(np.random.choice(
            set_replies,
            size=N_POSSIBLE_REPLIES-1, replace=False))
    possible_replies = np.array(possible_replies)
    np.random.shuffle(possible_replies)
    return possible_replies


def get_historic(user_id, t):

    # Get historic
    entries_question = \
        Question.objects.filter(user_id=user_id).order_by('t')

    hist_question = np.zeros(t, dtype=int)
    hist_success = np.zeros(t, dtype=bool)
    for i, e in enumerate(entries_question):
        hist_question[i] = e.question
        hist_success[i] = e.success

    return hist_question, hist_success


@Atomic
def _create_teacher(user_id, n_item):

    teacher = Leitner(user_id=user_id, n_item=n_item)
    teacher.save()
    return teacher.id, teacher


def _register_question(r):

    question = Question(
        user_id=r.user_id,
        t=r.t,
        question=r.id_question,
        reply=r.id_reply,
        success=r.success,
        time_display=_convert_to_time(r.time_display),
        time_reply=_convert_to_time(r.time_reply),
        possible_replies=r.id_possible_replies
    )
    question.save()
