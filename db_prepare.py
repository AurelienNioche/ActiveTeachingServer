import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from teaching_material.db_operation import fill_kanji_table
from teaching_material.models import WaniKani, Kanji, Meaning

from learner.models import User

from ActiveTeachingServer.credentials import \
    EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD

from ActiveTeachingServer.settings import DATABASES

DB_NAME = DATABASES['default']['NAME']


def import_from_wk():

    Meaning.objects.all().delete()

    wk = WaniKani.objects.all().order_by("level")

    new_entries = []
    for e in wk:

        m_entries = Meaning.objects.filter(meaning=e.meaning[0])
        if m_entries:
            m = m_entries[0]
        else:
            m = Meaning.objects.create(meaning=e.meaning[0])

        new_entries.append(Kanji(
            kanji=e.character,
            meaning=m
        ))

    Kanji.objects.bulk_create(new_entries)


def main():
    os.system("createdb ActiveTeaching --owner postgres")
    os.system("python3 manage.py makemigrations")
    os.system("python3 manage.py migrate")
    fill_kanji_table()
    User.objects.create_superuser(f'{EMAIL_HOST_USER}',
                                  f'{EMAIL_HOST_PASSWORD}')


if __name__ == "__main__":
    main()
