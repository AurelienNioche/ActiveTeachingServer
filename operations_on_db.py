import os

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

    if km != '-':
        out = split(km)
    else:
        out = split(on)

    assert out != '-'

    return out.capitalize()


def main():

    for e in Kanjilist.objects.all():

        km = e.translation_of_kun
        om = e.translation_of_on

        m = extract_single_meaning(km, om)

        print(e.id)
        e.meaning = m
        e.save()


if __name__ == "__main__":

    main()
