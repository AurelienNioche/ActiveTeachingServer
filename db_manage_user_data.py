import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from user_data.models import Question, User
from teacher.models import Leitner

from utils import AskUser


def backup_user_data():
    os.system(
        'pg_dump '
        '--data-only  '
        '--table question '
        '--table user '
        '--table teacher '
        'ActiveTeaching '
        '--inserts '
        '> data/user_and_question_tables.sql')


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

    os.system('psql ActiveTeaching < data/user_and_question_tables.sql')


def load_user_data():

    print("WARNING: loading user data will erase previous data if any.")
    _load_user_data()


def delete_user_data():

    print("WARNING: ALL USER DATA WILL BE ERASED")
    _delete_user_data()


if __name__ == "__main__":
    delete_user_data()
