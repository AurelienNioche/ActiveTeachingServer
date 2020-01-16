import numpy as np

from teaching_material.models import Kanji

try:
    kanji, meaning = \
        np.array(
            Kanji.objects.values_list('kanji', 'meaning').order_by('index')
        ).T

    unique_meaning, ___idx___, __inverse__ = np.unique(meaning,
                                                       return_index=True,
                                                       return_inverse=True)

    id_kanji = np.arange(len(kanji))
    id_meaning = id_kanji[___idx___][__inverse__]

except:
    raise Exception("Cannot load the database content!\n"
                    "Did you upload the kanji?")

# assert len(id_kanji) == len(id_meaning)
# for i in range(len(id_kanji)):
#     assert meaning[id_meaning[i]] == meaning[i]

# print(kanji)
# print(meaning)


def total_number_of_items():
    return Kanji.objects.count()


def get_string_representation(id_question, id_possible_replies):

    question = kanji[id_question]
    possible_replies = [meaning[i] for i in id_possible_replies]
    return question, possible_replies


def get_id():

    return id_kanji, id_meaning
