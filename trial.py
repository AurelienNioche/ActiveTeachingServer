import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
import json

from teaching_material.models import WaniKani

def import_from_wk():

    r = \
        requests.get(f"https://www.wanikani.com/api/"
                     f"user/bb7eb20355d4d3c2eacdb120901fb47d/kanji/"
                     f"{','.join([str(i) for i in range(1, 61)])}")

    with open('wanikani.json', 'w', encoding='utf-8') as f:
        json.dump(r.json(), f, ensure_ascii=False, indent=4)

def main():
    with open('wanikani.json', 'r', encoding='utf-8') as f:
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


if __name__ == "__main__":
    main()
