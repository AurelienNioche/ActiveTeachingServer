import os

from ActiveTeachingServer.settings import DATABASES
from teaching_material.models import Kanji, Meaning
from tools.utils import AskUser


DB_NAME = DATABASES['default']['NAME']


def has_numbers(string):

    return any(char.isdigit() for char in string)


def split(meanings):

    m = meanings.split(";")[0].split(",")[0]  # .split('(')[0]

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

        m = extract_single_meaning(km=e.translation_of_kun,
                                   on=e.translation_of_on)

        # import googletrans
        # tr = googletrans.Translator()
        # m = tr.translate(e.kanji, src='ja', dest='en').text
        # m = m.capitalize()

        e.meaning = m
        e.save()


# def create_index():
#
#     entries = Kanji.objects.all().order_by('grade')
#     for i, e in enumerate(entries):
#         e.index = i
#         e.save()


def load_backup_table(model):

    command = \
        f'pg_restore  -d {DB_NAME} --data-only data/{model.__name__}.dump'
    print(f"Run command '{command}'")
    os.system(command)


def backup_table(model):
    command = \
        f'pg_dump -Fc --column-inserts --data-only ' \
        f'--table {model._meta.db_table} ' \
        f'{DB_NAME} ' \
        f'> data/{model.__name__}.dump'

    print(f"Run command '{command}'")
    os.system(command)


@AskUser
def fill_kanji_table():

    Meaning.objects.all().delete()
    Kanji.objects.all().delete()
    load_backup_table(Meaning)
    load_backup_table(Kanji)


@AskUser
def backup_teaching_material():

    backup_table(Kanji)
    backup_table(Meaning)
