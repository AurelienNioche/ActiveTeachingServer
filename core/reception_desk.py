import numpy as np
from datetime import datetime

from learner.models import Question, User
from teaching_material.models import Meaning, Kanji

from core.task_parameters import N_POSSIBLE_REPLIES
from teaching_material.selection import JapaneseMaterial
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
                 id_correct_reply=None,
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
        self.id_correct_reply = id_correct_reply
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
                     id_correct_reply, question, possible_replies,
                     is_new_question,
                     n_iteration,
                     t):

        self.id_question = id_question
        self.id_reply = id_reply
        self.id_possible_replies = id_possible_replies
        self.id_correct_reply = id_correct_reply
        self.question = question
        self.possible_replies = possible_replies
        self.is_new_question = is_new_question
        self.n_iteration = n_iteration
        self.t = t

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

    id_questions, id_replies = JapaneseMaterial.get_id()
    n_item = JapaneseMaterial.N_ITEM

    if r.subject == Request.SIGN_UP:

        user_id = learner.authentication.sign_up(r, n_item)
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
            register_user_reply(r)

        else:
            raise ValueError(
                f"Subject of the request not recognized: '{r.subject}'")

        if r.ok:

            user = User.objects.get(id=r.user_id)

            # teacher_name = reply['teacher']

            # first_call = reply['userId'] == USER_DEFAULT_ID

            # assert teacher_name == 'leitner', 'Only Leitner teacher is implemented!'

            hist_id_question, hist_id_reply, hist_success = \
                get_historic(user=user)
            r.t = len(hist_id_question)

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
                    r.set_question(
                        id_question=not_replied.question.id,
                        id_possible_replies=
                        [p.id for p in not_replied.possible_replies.all()],
                        id_correct_reply=not_replied.correct_reply.id,
                        question=not_replied.question.kanji,
                        possible_replies=[p.meaning for p in not_replied.possible_replies.all()],
                        is_new_question=not_replied.kanji.id not in hist_id_question,
                        n_iteration=N_ITERATION,
                        t=len(hist_id_question)
                    )

                else:
                    raise NotImplementedError

    return r.to_json_serializable_dic()


# def _random_question(id_questions):
#     id_question = np.random.randint(len(id_questions))
#     return id_question


def new_question(user,
                 id_questions,
                 id_replies,
                 hist_id_question,
                 hist_id_reply,
                 hist_success,
                 item_model,
                 reply_model):

    # Get teacher
    t = len(hist_id_question)
    print("user", user, "t", t)
    teacher = user.leitner
    id_item = teacher.ask(
        t=t,
        hist_success=hist_success,
        hist_question=hist_id_question,
        questions=id_questions)
    teacher.save()

    item = item_model.objects.get(id=id_item)

    id_possible_replies = get_id_possible_replies(
        id_replies=id_replies,
        hist_id_reply=hist_id_reply,
        id_correct_reply=id_item
    )

    question_entry = Question(
        user=user,
        t=t,
        question=item,
    )
    question_entry.save()
    for id_pr in id_possible_replies:
        question_entry.possible_replies.add(reply_model.objects.get(id=id_pr))
    # question_entry.save()

    return question_entry


def get_id_possible_replies(
        id_replies, id_correct_reply,
        hist_id_reply):

    """
    Select randomly possible replies, including the correct one
    """
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
    return id_possible_replies


def get_historic(user):

    # Get historic
    entries_question = user.question_set.all().order_by('t')

    t = len(entries_question)

    hist_id_question = np.zeros(t, dtype=int)
    hist_id_reply = np.zeros(t, dtype=int)
    hist_success = np.zeros(t, dtype=bool)
    for i, e in enumerate(entries_question):
        hist_id_question[i] = e.question.id
        hist_success[i] = e.success
        hist_id_reply[i] = e.question.meaning.id


    return hist_id_question, hist_id_reply, hist_success


def get_question_not_answered(user):

    entries_not_answered = user.question_set.filter(reply=None)
    if entries_not_answered:
        return entries_not_answered[0]
    else:
        return None


def register_user_reply(user, r):

    question = Question.objects.get(user=user, t=r.t)
    question.reply = Meaning.objects.get(id=r.id_reply)
    question.success = r.success
    question.time_display = convert_to_time(r.time_display)
    question.time_reply = convert_to_time(r.time_reply)
    question.save()


def convert_to_time(string_time):
    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')
