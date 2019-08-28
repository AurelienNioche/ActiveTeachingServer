import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from ActiveTeachingServer.settings import DATABASES
from user_data.models import Question, User
from teacher.models import Leitner

from utils import AskUser

BKP_FILE = os.path.join("data", "user_and_question_tables.sql")
DB_NAME = DATABASES['default']['NAME']


def backup_user_data():
    os.system(
        'pg_dump '
        '--data-only  '
        f'--table {Question._meta.db_table} '
        f'--table {User._meta.db_table} '
        f'--table {Leitner._meta.db_table} '
        f'{DB_NAME} '
        '--inserts '
        f'> {BKP_FILE}.sql')


@AskUser
def _delete_user_data():
    Question.objects.all().delete()
    User.objects.all().delete()
    Leitner.objects.all().delete()


@AskUser
def _load_user_data():
    Question.objects.all().delete()
    User.objects.all().delete()
    Leitner.objects.all().delete()

    os.system(f'psql {DB_NAME} < {BKP_FILE}')


def load_user_data():

    print("WARNING: loading user data will erase previous data if any.")
    _load_user_data()


def delete_user_data():

    print("WARNING: ALL USER DATA WILL BE ERASED")
    _delete_user_data()


if __name__ == "__main__":
    delete_user_data()
