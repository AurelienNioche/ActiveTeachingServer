import numpy as np
from datetime import datetime

from user_data.models import Question, User

from task.fixed_parameters import N_POSSIBLE_REPLIES
import teaching_material.selection

from teacher.models import Leitner

from utils import Atomic

USER_DEFAULT_ID = -1
USER_TEST_ID = -2


def get_question(reply):

    # Get task parameters
    register_replies = reply['registerReplies']
    t_max = reply['nIteration']
    teacher_name = reply['teacher']
    user_id = reply['userId']
    t = reply['t']

    first_call = reply['userId'] == USER_DEFAULT_ID

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

    id_questions, id_replies = teaching_material.selection.get_id()

    if register_replies:
        id_question = \
            _new_question(user_id=user_id, t=t,
                          id_questions=id_questions
                          )

    else:
        id_question = \
            _random_question(id_questions=id_questions,
                             id_replies=id_replies)

    id_reply = id_replies[id_question]

    id_possible_replies = \
        Leitner.get_possible_replies(
            correct_reply=id_reply,
            replies=id_replies,
            n_possible_replies=N_POSSIBLE_REPLIES)

    question, possible_replies = \
        teaching_material.selection.get_string_representation(
            id_question=id_question,
            id_possible_replies=id_possible_replies
        )

    to_return = {
        'userId': int(user_id),
        't': int(t),
        'nIteration': int(t_max),
        'registerReplies': register_replies,
        'question': question,
        'possibleReplies': possible_replies,
        'idQuestion': int(id_question),
        'idCorrectAnswer': int(id_reply),
        'idPossibleReplies': [int(i) for i in id_possible_replies],
    }
    print("Ready to send!")
    return to_return


def _convert_to_time(string_time):

    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')


def _random_question(id_questions):
    id_question = np.random.randint(len(id_questions))
    return id_question


def _new_question(user_id, t, id_questions):

    if t == 0:
        # Create teacher
        teacher_id, teacher = _create_teacher(user_id=user_id,
                                              n_item=len(id_questions))
        question_id = teacher.ask(t=t, questions=id_questions)
        teacher.save()

    else:

        # Get historic
        entries_question = \
            Question.objects.filter(user_id=user_id).order_by('t')

        hist_question = np.zeros(t, dtype=int)
        hist_success = np.zeros(t, dtype=bool)
        for i, e in enumerate(entries_question):
            hist_question[i] = e.question
            hist_success[i] = e.success

        print('hist question', hist_question)
        print('hist success', hist_success)

        # Get teacher
        teacher = Leitner.objects.get(user_id=user_id)
        question_id = teacher.ask(
            t=t,
            hist_success=hist_success,
            hist_question=hist_question,
            questions=id_questions)
        teacher.save()

    return question_id


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

