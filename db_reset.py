import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from learner.models import User

from ActiveTeachingServer.credentials import \
    EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD

import os

from tools.utils import AskUser

from teaching_material.db_operation import fill_kanji_table


@AskUser
def reset():

    os.system("dropdb ActiveTeaching")
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')

    os.system("createdb ActiveTeaching --owner postgres")
    os.system("python3 manage.py makemigrations")
    os.system("python3 manage.py migrate")
    fill_kanji_table()
    User.objects.create_superuser(f'{EMAIL_HOST_USER}',
                                  f'{EMAIL_HOST_PASSWORD}')


if __name__ == "__main__":

    reset()
