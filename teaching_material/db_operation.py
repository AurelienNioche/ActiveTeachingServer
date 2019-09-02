import os

from ActiveTeachingServer.settings import DATABASES
from teaching_material.models import Kanji
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


def create_index():

    entries = Kanji.objects.all().order_by('grade')
    for i, e in enumerate(entries):
        e.index = i
        e.save()


@AskUser
def backup_kanji_table(bkp_file=os.path.join("data", "kanji_table.sql")):

    command = \
        f'pg_dump ' \
        f'--table {Kanji._meta.db_table} ' \
        f'{DB_NAME} ' \
        f'--inserts ' \
        f'--clean ' \
        f'> {bkp_file}'

    print(f"Run command '{command}'")
    os.system(command)


@AskUser
def fill_kanji_table(bkp_file=os.path.join("data", "kanji_table.sql")):

    # Kanji.objects.all().delete()
    command = f'psql {DB_NAME} < {bkp_file}'
    print(f"Run command '{command}'")
    os.system(command)
