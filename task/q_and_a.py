import numpy as np
from datetime import datetime

from . models import Kanji, User, Question, Parameter, PredefinedQuestion

from . parameters import n_possible_replies
from utils import Atomic


def get_question(reply):

    if reply['userId'] == -1:
        user_id = _register_user()
        t = 0

    else:
        user_id, t = _register_response(reply)
        t += 1

    # Check for t_max
    t_max = Parameter.objects.get(name='t_max').value
    if t == t_max:
        return {
            't': -1
        }

    if Parameter.objects.get(name='use_predefined_question').value == 1:
        q, correct_answer, correct_answer_idx, possible_replies = _load_predefined_question(t)

    else:
        q, correct_answer, correct_answer_idx, possible_replies = _prepare_new_question()

    # Register new question
    _register_question(user_id=user_id, t=t, question=q, correct_answer=correct_answer,
                       possible_replies=possible_replies)

    # Return dic for JSON reply to client
    question_dic = {
        'userId': user_id,
        't': t,
        'tMax': t_max,
        'question': q,
        'correctAnswer': correct_answer,
        'correctAnswerIdx': correct_answer_idx,
        'possibleReplies': possible_replies
    }

    return question_dic


def _convert_to_time(string_time):

    return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')


def _register_response(reply):

    user_id = reply['userId']
    t = reply['t']

    question = Question.objects.get(user_id=user_id, t=t)
    question.reply = reply['reply']
    question.time_display = _convert_to_time(reply['timeDisplay'])
    question.time_reply = _convert_to_time(reply['timeReply'])
    question.save(force_update=True)

    return user_id, t


def _prepare_new_question():

    k = list(Kanji.objects.all())

    while True:
        idx = np.random.choice(np.arange(len(k)), size=6, replace=False)

        possible_replies = [k[idx[i]].meaning for i in range(6)]
        print(possible_replies)
        if len(np.unique(possible_replies)) == len(possible_replies):
            break

    question = k[idx[0]].kanji
    correct_answer = k[idx[0]].meaning

    np.random.shuffle(possible_replies)

    correct_answer_idx = possible_replies.index(correct_answer)

    return question, correct_answer, correct_answer_idx, possible_replies


def _load_predefined_question(t):

    question_entry = PredefinedQuestion.objects.get(t=t)

    question = question_entry.question
    correct_answer = question_entry.correct_answer
    possible_replies = [
        getattr(question_entry, f'possible_reply_{i}') for i in range(n_possible_replies)
    ]

    correct_answer_idx = possible_replies.index(correct_answer)

    return question, correct_answer, correct_answer_idx, possible_replies


@Atomic
def _register_user():

    """
    Creates a new user and returns its instance
    """

    u = User()

    u.save()
    return u.id


@Atomic
def _register_question(user_id, t, question, correct_answer, possible_replies):

    """
    Creates a new user and returns its instance
    """

    q = Question()
    q.user_id = user_id
    q.t = t
    q.question = question
    q.correct_answer = correct_answer

    for i in range(n_possible_replies):
        setattr(q, f'possible_reply_{i}', possible_replies[i])

    q.save()
    return q.id
