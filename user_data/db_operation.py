import os

from ActiveTeachingServer.settings import DATABASES
from teacher.models import Leitner
from user_data.models import Question, User
from tools.utils import AskUser

BKP_FILE = os.path.join("data", "user_and_question_tables.sql")
DB_NAME = DATABASES['default']['NAME']


def backup_user_data():

    command = \
        'pg_dump ' \
        f'--table {Question._meta.db_table} ' \
        f'--table {User._meta.db_table} ' \
        f'--table {Leitner._meta.db_table} ' \
        f'{DB_NAME} ' \
        f'--inserts ' \
        f'--clean ' \
        f'> {BKP_FILE}'

    print(f"Run command '{command}'")
    os.system(command)


@AskUser
def _delete_user_data():
    Question.objects.all().delete()
    User.objects.all().delete()
    Leitner.objects.all().delete()


@AskUser
def _load_user_data():

    command = f'psql {DB_NAME} < {BKP_FILE}'
    print(f"Run command '{command}'")
    os.system(command)


def load_user_data():

    print("WARNING: loading user data will erase previous data if any.")
    _load_user_data()


def delete_user_data():

    print("WARNING: ALL USER DATA WILL BE ERASED")
    _delete_user_data()