import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
import json

from ActiveTeachingServer.settings import DATABASES
from teaching_material.models import WaniKani, Kanji, Meaning


DB_NAME = DATABASES['default']['NAME']
WK_BKP = os.path.join('data', 'wanikani.json')


def import_from_web():

    r = \
        requests.get(f"https://www.wanikani.com/api/"
                     f"user/bb7eb20355d4d3c2eacdb120901fb47d/kanji/"
                     f"{','.join([str(i) for i in range(1, 61)])}")

    data = r.json()

    with open(WK_BKP, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data


def create_wk_entries():

    if not os.path.exists(WK_BKP):
        data = import_from_web()

    else:
        with open('data/wanikani.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

    entries = []
    for d in data['requested_information']:
        d.pop("user_specific", None)
        for k in ("meaning","onyomi", "kunyomi", "nanori"):
            if d[k] is None:
                d.pop(k)
            else:
                d[k] = d[k].split(", ")
        entries.append(WaniKani(**d))

    WaniKani.objects.bulk_create(entries)


def import_from_wk():

    wk = WaniKani.objects.all().order_by("level")
    if not wk.count():
        create_wk_entries()

    wk = WaniKani.objects.all().order_by("level")

    Meaning.objects.all().delete()
    Kanji.objects.all().delete()

    new_entries = []
    for e in wk:

        m_entries = Meaning.objects.filter(meaning=e.meaning[0])
        if m_entries:
            m = m_entries[0]
        else:
            m = Meaning.objects.create(meaning=e.meaning[0])

        new_entries.append(Kanji(
            value=e.character,
            meaning=m
        ))

    Kanji.objects.bulk_create(new_entries)


def main():

    import_from_wk()


if __name__ == "__main__":
    main()
