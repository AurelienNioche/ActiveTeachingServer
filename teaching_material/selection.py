import numpy as np

from teaching_material.models import Kanji


class JapaneseMaterial:

    KANJI = Kanji.objects.all().order_by('id')
    KANJI_ID = np.array([k.id for k in KANJI])

    MEANING = np.array([k.meaning.meaning for k in KANJI])
    MEANING_ID = np.array([k.meaning.id for k in KANJI])

    N_ITEM = len(KANJI)

    @classmethod
    def total_number_of_items(cls):
        return cls.N_ITEM

    @classmethod
    def get_string_representation(cls, id_question, id_possible_replies):

        question = cls.KANJI[id_question]
        possible_replies = [cls.KANJI[i] for i in id_possible_replies]
        return question, possible_replies

    @classmethod
    def get_id(cls):

        return cls.KANJI_ID, cls.MEANING_ID

