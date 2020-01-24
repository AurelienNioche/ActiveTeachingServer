import numpy as np
from datetime import datetime

from learner.models import Question, User

from core.task_parameters import N_POSSIBLE_REPLIES
import teaching_material.selection
import learner.authentication


USER_DEFAULT_ID = -1
USER_TEST_ID = -2

N_ITERATION = 150


class Request:

    LOGIN = "login"
    SIGN_UP = "sign_up"
    QUESTION = "question"

    def __init__(self, subject,
                 msg=None,
                 ok=None,
                 n_iteration=None, user_id=None,
                 t=-1,
                 email=None,
                 password=None,
                 question=None,
                 possible_replies=None,
                 id_question=None,
                 id_reply=None,
                 is_new_question=None,
                 id_correct_answer=None,
                 success=None,
                 time_display=None,
                 time_reply=None,
                 gender=None,
                 mother_tongue=None,
                 other_language=None,
                 id_possible_replies=None):

        self.subject = subject
        self.ok = ok
        self.msg = msg

        self.n_iteration = n_iteration
        self.user_id = user_id
        self.t = t

        self.id_reply = id_reply
        self.id_question = id_question
        self.id_possible_replies = id_possible_replies
        self.idx_correct_answer = id_correct_answer
        self.is_new_question = is_new_question
        self.question = question
        self.possible_replies = possible_replies

        self.success = success
        self.time_display = time_display
        self.time_reply = time_reply

        self.email = email
        self.password = password
        self.gender = gender
        self.mother_tongue = mother_tongue
        self.other_language = other_language

    def set_question(self, id_question, id_reply, id_possible_replies,
                     idx_correct_answer, question, possible_replies,
                     is_new_question):

        self.id_question = id_question
        self.id_reply = id_reply
        self.id_possible_replies = id_possible_replies
        self.idx_correct_answer = idx_correct_answer
        self.question = question
        self.possible_replies = possible_replies
        self.is_new_question = is_new_question

    def to_json_serializable_dic(self):

        dic = self.__dict__
        for (k, v) in dic.items():
            if type(v) == np.ndarray:
                dic[k] = [int(i) for i in v]
            elif type(v) == np.int64:
                dic[k] = int(v)

        return dic

    # def return_to_user(self, question, possible_replies, id_question,
    #                    id_possible_replies, id_reply, is_new_question):
    #     return {
    #         'userId': int(self.user_id),
    #         't': int(self.t),
    #         'nIteration': int(self.n_iteration),
    #         'question': question,
    #         'possibleReplies': possible_replies,
    #         'idQuestion': int(id_question),
    #         'newQuestion': is_new_question,
    #         'idCorrectAnswer': int(id_reply),
    #         'idPossibleReplies': [int(i) for i in id_possible_replies],
    #     }


def treat_request(request_kwargs):

    r = Request(**request_kwargs)

    id_questions, id_replies = teaching_material.selection.get_id()

    if r.subject == Request.SIGN_UP:

        user_id = learner.authentication.sign_up(r, len(id_questions))
        if user_id != -1:
            r.ok = True
            r.user_id = user_id

        else:
            r.ok = False
            r.msg = "User already exists!"

    else:

        if r.subject == Request.LOGIN:
            user_id = learner.authentication.login(r)
            if user_id < 0:
                r.ok = False
            else:
                r.user_id = user_id
                r.ok = True

        elif r.subject == Request.QUESTION:
            register_question(r)

        else:
            raise ValueError(
                f"Subject of the request not recognized: '{r.subject}'")

        if r.ok:

            user = User.objects.get(id=r.user_id)

            # teacher_name = reply['teacher']

            # first_call = reply['userId'] == USER_DEFAULT_ID

            # assert teacher_name == 'leitner', 'Only Leitner teacher is implemented!'

            hist_question, hist_success = get_historic(user=user)
            r.t = len(hist_question)

            # Check for t_max
            if r.t == r.n_iteration:
                r.t = -1

            else:

                # TODO: redirect if sign up

                # TODO: redirect if login

                # TODO:  is the learner is authorized to play?

                # TODO: which material should he use?

                # TODO: which teacher should he use?

                not_replied = get_question_not_answered(user)

                if not_replied is not None:
                    r.set_question(not_replied)

                r.id_question = \
                    new_question(
                        user=user,
                        hist_question=hist_question,
                        hist_success=hist_success,
                        id_questions=id_questions)

                r.id_reply = id_replies[r.id_question]

                r.id_possible_replies = \
                    get_possible_replies(
                        hist_question=hist_question,
                        id_reply=r.id_reply,
                        id_replies=id_replies
                    )

                r.question, r.possible_replies = \
                    teaching_material.selection.get_string_representation(
                        id_question=r.id_question,
                        id_possible_replies=r.id_possible_replies
                    )

                r.id_correct_answer = list(r.id_possible_replies).index(r.id_reply)
                r.is_new_question = r.id_question not in hist_question

                r.t = len(hist_question)
                r.n_iteration = N_ITERATION

    return r.to_json_serializable_dic()


# def _random_question(id_questions):
#     id_question = np.random.randint(len(id_questions))
#     return id_question


def new_question(user, id_questions,
                 hist_question, hist_success):

    # Get teacher
    t = len(hist_question)
    print("user", user, "t", t)
    teacher = user.leitner
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


def get_historic(user):

    # Get historic
    entries_question = user.question_set.all().order_by('t')

    t = len(entries_question)

    hist_question = np.zeros(t, dtype=int)
    hist_success = np.zeros(t, dtype=bool)
    for i, e in enumerate(entries_question):
        hist_question[i] = e.question
        hist_success[i] = e.success

    return hist_question, hist_success


def get_question_not_answered(user):

    entries_not_answered = user.question_set.filter(reply=-1)
    if entries_not_answered:
        return entries_not_answered[0]
    else:
        return None


def register_question(user, r):

    question = Question(
        user=user,
        t=r.t,
        question=r.id_question,
        reply=r.id_reply,
        success=r.success,
        time_display=convert_to_time(r.time_display),
        time_reply=convert_to_time(r.time_reply),
        possible_replies=r.id_possible_replies
    )
    question.save()


def convert_to_time(string_time):
    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')
