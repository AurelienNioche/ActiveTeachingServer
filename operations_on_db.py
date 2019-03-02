import os
import numpy as np

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import Kanjilist


def has_numbers(string):

    return any(char.isdigit() for char in string)


def split(meanings):

    m = meanings.split(";")[0].split(",")[0].split('(')[0]

    if not has_numbers(m):
        m = m.split('.')[0]

    if m == "A":
        m = "first"
    elif m == "B":
        m = "second"
    elif m == "C":
        m = "third"

    return m


def extract_single_meaning(km, on):

    if km not in ('-', ' ', ''):
        out = split(km)
    else:
        out = split(on)

    assert out not in ('-', '')

    return out.capitalize()


def main():

    ms = []

    for e in Kanjilist.objects.all():

        km = e.translation_of_kun
        om = e.translation_of_on

        m = extract_single_meaning(km, om)

        # print(e.id)
        e.meaning = m
        e.save()

        ms.append(m)

    # Get common significations
    from collections import Counter
    c = Counter(ms)

    element_in_double = [k for k, v in c.items() if v > 1]

    for me in element_in_double:
        for e in Kanjilist.objects.filter(meaning=me):

            print(e.kanji)
            print(e.meaning)
            print(e.translation_of_kun)
            print(e.translation_of_on)




if __name__ == "__main__":

    main()
