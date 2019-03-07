import os
import django.db.utils
import psycopg2
import googletrans

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import Kanji, Parameter

from operations_on_db import AskUser


def has_numbers(string):

    return any(char.isdigit() for char in string)


def split(meanings):

    m = meanings.split(";")[0].split(",")[0] # .split('(')[0]

    if not has_numbers(m):
        m = m.split('.')[0]

    if m == "A":
        m = "first"
    elif m == "B":
        m = "second"
    elif m == "C":
        m = "third"

    m = m[0].upper() + m[1:]
    if m[0] == '(':
        m = m[0] + m[1].upper() + m[2:]

    return m


def extract_single_meaning(km, on):

    if km not in ('-', ' ', ''):
        out = split(km)
    else:
        out = split(on)

    assert out not in ('-', '')

    return out


def get_common_significations():

    ms = [e.meaning for e in Kanji.objects.order_by('id')]

    from collections import Counter
    c = Counter(ms)

    element_in_double = [k for k, v in c.items() if v > 1]

    for me in element_in_double:
        for e in Kanji.objects.filter(meaning=me):

            print(e.kanji)
            print(e.meaning)
            print(e.translation_of_kun)
            print(e.translation_of_on)


def fill_single_meaning_column():

    for e in Kanji.objects.order_by('id'):

        print(e.id)

        m = extract_single_meaning(km=e.translation_of_kun, on=e.translation_of_on)

        # tr = googletrans.Translator()
        # m = tr.translate(e.kanji, src='ja', dest='en').text
        # m = m.capitalize()

        e.meaning = m
        e.save()


@AskUser
def fill_kanji_table():

    os.system('psql ActiveTeaching < data/kanji_table.sql')
    # os.system('psql ActiveTeaching < data/kanji_content.sql')


def add_default_parameters(t_max=100, use_predefined_question=0, test=0):

    try:
        p = Parameter()
        p.name = "t_max"
        p.value = t_max
        p.save()

        p = Parameter()
        p.name = "use_predefined_question"
        p.value = use_predefined_question
        p.save()

        p = Parameter()
        p.name = "test"
        p.value = test
        p.save()

    except (django.db.IntegrityError,
            django.db.OperationalError,
            django.db.utils.OperationalError,
            psycopg2.IntegrityError,
            psycopg2.OperationalError):
        print("Parameters seem to have already been set.")


def main():

    fill_kanji_table()
    add_default_parameters()

    # # Get common significations
    # get_common_significations()


if __name__ == "__main__":

    main()
    # User.objects.all().delete()
