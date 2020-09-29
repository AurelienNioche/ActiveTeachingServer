import numpy as np

from config import config

from teaching_material.models.kanji import Kanji
from user.models.user import User


def run(previous_email=None):

    if previous_email is not None:
        u = User.objects.filter(email=previous_email).first()
        m = []
        for te in u.teachingengine_set.all():
            for m_id in list(te.material.values_list('id', flat=True)):
                m.append(m_id)
        material = list(Kanji.objects.exclude(id__in=m))
    else:
        material = list(Kanji.objects.all())

    selection = np.random.choice(
        material, size=config.N_ITEM * 2,
        replace=False)

    leitner_m = selection[:config.N_ITEM]
    active_teaching_m = selection[config.N_ITEM:]

    return leitner_m, active_teaching_m
