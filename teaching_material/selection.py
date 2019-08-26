import numpy as np

from teaching_material.models import Kanji


def total_number_of_items():
    return Kanji.objects.count()


def get_string_representation(idx_question, idx_reply):

    entries = Kanji.objects.order_by('id')
    kanji = np.array([i.kanji for i in entries])[idx_question]
    meanings = np.array([i.meaning for i in entries])[idx_reply]

    return kanji, meanings


def get():

    n = Kanji.objects.count()
    entries = Kanji.objects.order_by('id')
    str_questions = [e.kanji for e in entries]
    str_replies = [e.meaning for e in entries]
    questions = np.arange(n)
    uniq_string, replies = np.unique(
        str_replies, return_inverse=True)
    return questions, replies, str_questions, str_replies
