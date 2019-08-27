import numpy as np

from teaching_material.models import Kanji

__id__, strokes = \
    np.array(Kanji.objects.values_list('id', 'strokes').order_by('id')).T
kanji, meaning = \
    np.array(Kanji.objects.values_list('kanji', 'meaning')
                          .order_by('id')).T

unique_meaning, ___idx___, __inverse__ = np.unique(meaning,
                                                   return_index=True,
                                                   return_inverse=True)

id_kanji = __id__
id_meaning = __id__[___idx___][__inverse__]

# str_questions = np.zeros(n, dtype=str)
# str_replies = np.zeros(n, dtype=str)
#
# [e.kanji for e in entries]
# str_replies = [e.meaning for e in entries]
#
# id_questions = [e.id for e in entries]

print(kanji)
print(meaning)


def total_number_of_items():
    return Kanji.objects.count()


def get_string_representation(id_question, id_possible_replies):

    question = kanji[__id__ == id_question][0]
    possible_replies = [meaning[np.where(__id__ == i)[0][0]]
                        for i in id_possible_replies]
    return question, possible_replies


def get_id():

    return id_kanji, id_meaning
