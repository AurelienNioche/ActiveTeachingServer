import numpy as np
from django.db import transaction
import threading
import django.db.utils
import psycopg2
from datetime import datetime

from . models import Kanji, User, Question


class Atomic:

    def __init__(self, f):
        self.f = f

    def __call__(self, **kwargs):

        while True:
            try:

                with transaction.atomic():
                    return self.f(**kwargs)

            except (
                    django.db.IntegrityError,
                    django.db.OperationalError,
                    django.db.utils.OperationalError,
                    psycopg2.IntegrityError,
                    psycopg2.OperationalError
            ) as e:
                print("*" * 50)
                print("INTEGRITY ERROR" + "!" * 10)
                print(str(e))
                print("*" * 50)
                threading.Event().wait(1 + np.random.random() * 4)
                continue


def get_question(reply):

    # a = datetime.strptime("2019-03-05 14:38:15.324397", '%Y-%m-%d %H:%M:%S.%f')

    if reply['userId'] == -1:
        user_id = _create_new_user()
        t = 0
    else:
        user_id = reply['userId']

        # TODO: Register response

        t = reply['questionId'] + 1

    # Prepare new question
    k = list(Kanji.objects.all())

    while True:
        idx = np.random.choice(np.arange(len(k)), size=6, replace=False)

        possible_replies = [k[idx[i]].meaning for i in range(6)]
        print(possible_replies)
        if len(np.unique(possible_replies)) == len(possible_replies):
            break

    q = k[idx[0]].kanji
    correct_answer = k[idx[0]].meaning

    np.random.shuffle(possible_replies)

    correct_answer_idx = possible_replies.index(correct_answer)

    # Register new question
    _create_new_question(user_id=user_id, t=t, question=q, correct_answer=correct_answer,
                         possible_replies=possible_replies)

    # Return dic for JSON reply to client
    question = {
        'userId': user_id,
        'questionId': t,
        'question': q,
        'correctAnswer': correct_answer,
        'correctAnswerIdx': correct_answer_idx,
        'possibleReplies': possible_replies
    }

    return question


@Atomic
def _create_new_user():

    """
    Creates a new user and returns its instance
    """

    u = User()

    u.save()
    return u.id


@Atomic
def _create_new_question(user_id, t, question, correct_answer, possible_replies):

    """
    Creates a new user and returns its instance
    """

    q = Question(
        user_id=user_id,
        t=t,
        question=question,
        correct_answer=correct_answer,
        possible_reply_0=possible_replies[0],
        possible_reply_1=possible_replies[1],
        possible_reply_2=possible_replies[2],
        possible_reply_3=possible_replies[3],
        possible_reply_4=possible_replies[4],
        possible_reply_5=possible_replies[5],
    )

    q.save()
    return q.id
