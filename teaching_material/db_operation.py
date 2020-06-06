import os
from datetime import datetime
from glob import glob
import dateutil.parser

from ActiveTeachingServer.settings import DATABASES
from teaching_material.models import Kanji, Meaning
from utils.utils import AskUser


DB_NAME = DATABASES['default']['NAME']


def parse_date(dump_name):

    date_string = dump_name.split('_')[-1].replace(".dump", "")

    return dateutil.parser.parse(date_string)


def load_backup_table(model):

    files = glob(f'data/{model.__name__}_*.dump').sort()
    file_to_take = sorted(files, key=lambda x: parse_date(x), reverse=True)[0]

    command = \
        f'pg_restore  -d {DB_NAME} --data-only {file_to_take}'
    print(f"Run command '{command}'")
    os.system(command)


def backup_table(model):

    command = \
        f'pg_dump -Fc --column-inserts --data-only ' \
        f'--table {model._meta.db_table} ' \
        f'{DB_NAME} ' \
        f'> data/{model.__name__}_{datetime.utcnow().isoformat()}.dump'

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
