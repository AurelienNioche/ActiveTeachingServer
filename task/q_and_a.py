import numpy as np
from datetime import datetime

from . models import User, Question

from task.fixed_parameters import n_possible_replies
import teaching_material.selection

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

    # Check for t_max
    if t == t_max:
        return {
            't': -1
        }

    return \
        _new_question(user_id=user_id, t=t,
                      t_max=t_max, teacher_name=teacher_name)


def _convert_to_time(string_time):

    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')


def _new_question(user_id, t, t_max, teacher_name):

    # Get historic
    entries_question = Question.objects.filter(user_id=user_id).order_by('t')

    index_hist_question = np.zeros(t+1, dtype=int)
    index_hist_replies = np.zeros(t+1, dtype=int)
    index_hist_success = np.zeros(t+1, dtype=bool)
    for i, e in enumerate(entries_question):
        index_hist_question[i] = e.question
        index_hist_replies[i] = e.reply
        index_hist_success[i] = e.success

    questions, meanings = teaching_material.selection.get()

    # question = k[q_index_question].kanji
    # correct_answer = k[index_question].meaning
    #
    # possible_replies = [k[i].meaning for i in index_poss_replies]
    #
    # correct_answer_idx = possible_replies.index(correct_answer)
    #
    # # Return dic for JSON reply to client
    # question_dic = {
    #     'userId': user_id,
    #     't': t,
    #     'tMax': t_max,
    #     'question': q,
    #     'possibleReplies': possible_replies,
    #     'idxCorrectAnswer': correct_answer_idx,
    #     'idxPossibleReplies':
    # }


@Atomic
def _register_user():

    """
    Creates a new user and returns its instance
    """

    u = User()

    u.save()
    return u.id

@Atomic
def _register_question(reply):

    user_id = reply['userId']
    t = reply['t']
    success = reply['success']
    question = reply['question']
    reply__ = reply['reply']
    time_display = _convert_to_time(reply['timeDisplay'])
    time_reply = _convert_to_time(reply['timeReply'])

    q = Question()
    question = Question(
        user_id=user_id,
        t=t,
        question=question,
        reply=reply__,
        success=success,
        time_display=time_display,
        time_reply=time_reply
    )
    for i in range(n_possible_replies):
        setattr(q, f'possible_reply_{i}', reply[f'possible_reply_{i}'])

    question.save()

    return user_id, t



# def _load_predefined_question(t):
#
#     question_entry = PredefinedQuestion.objects.get(t=t)
#
#     question = question_entry.question
#     correct_answer = question_entry.correct_answer
#     possible_replies = [
#         getattr(question_entry, f'possible_reply_{i}') for i in range(n_possible_replies)
#     ]
#
#     correct_answer_idx = possible_replies.index(correct_answer)
#
#     return question, correct_answer, correct_answer_idx, possible_replies
