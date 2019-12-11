import numpy as np
from datetime import datetime

from user_data.models import Question, User

from core.fixed_parameters import N_POSSIBLE_REPLIES

# --- Need to be changed --- #
import teaching_material.selection
# ------------------------ #

from teacher.models import Leitner

from tools.utils import Atomic

USER_DEFAULT_ID = -1
USER_TEST_ID = -2


def get_question(reply):

    # Get task parameters
    register_replies = reply['registerReplies']
    t_max = reply['nIteration']
    teacher_name = reply['teacher']
    material = reply['material'] # Change this to finnish to use my material
    user_id = reply['userId']
    t = reply['t']

    first_call = reply['userId'] == USER_DEFAULT_ID

    assert material == 'japanese', 'Only Japanese material is implemented!'
    assert teacher_name == 'leitner', 'Only Leitner teacher is implemented!'

    # Check for t_max
    if t == t_max:
        return {
            't': -1
        }

    if first_call:
        if register_replies:
            user_id = _register_user()
        else:
            user_id = USER_TEST_ID
        t = 0

    else:
        if register_replies:
            _register_question(reply)
        t += 1

    # --- Need to be changed --- #
    id_questions, id_replies = teaching_material.selection.get_id()
    # --- Need to be changed --- #

    hist_question, hist_success = get_historic(user_id=user_id, t=t)

    if register_replies:
        id_question = \
            _new_question(
                user_id=user_id,
                t=t,
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

    # --- Need to be changed --- #
    question, possible_replies = \
        teaching_material.selection.get_string_representation(
            id_question=id_question,
            id_possible_replies=id_possible_replies
        )
    # --- Need to be changed --- #

    is_new_question = id_question not in hist_question

    to_return = {
        'userId': int(user_id),
        't': int(t),
        'nIteration': int(t_max),
        'registerReplies': register_replies,
        'question': question,
        'possibleReplies': possible_replies,
        'idQuestion': int(id_question),
        'newQuestion': is_new_question,
        'idCorrectAnswer': int(id_reply),
        'idPossibleReplies': [int(i) for i in id_possible_replies],
    }
    return to_return


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


@Atomic
def _register_user():

    """
    Creates a new user and returns its instance
    """

    u = User()

    u.save()
    return u.id


def _register_question(reply):

    user_id = reply['userId']
    t = reply['t']
    success = reply['success']
    id_question = reply['idQuestion']
    id_reply = reply['idReply']
    id_possible_replies = reply[f'idPossibleReplies']
    time_display = _convert_to_time(reply['timeDisplay'])
    time_reply = _convert_to_time(reply['timeReply'])

    question = Question(
        user_id=user_id,
        t=t,
        question=id_question,
        reply=id_reply,
        success=success,
        time_display=time_display,
        time_reply=time_reply,
        possible_replies=id_possible_replies
    )
    question.save()
