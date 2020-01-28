import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from teaching_material.db_operation import fill_kanji_table

from learner.models import User

from ActiveTeachingServer.credentials import \
    EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD

from ActiveTeachingServer.settings import DATABASES

DB_NAME = DATABASES['default']['NAME']


# entries = Kanji.objects.all().order_by('id')
# for e in entries:
#
#     m_entries = Meaning.objects.filter(meaning=e.meaning_string)
#     if m_entries:
#         m = m_entries[0]
#     else:
#         m = Meaning.objects.create(meaning=e.meaning_string)
#
#     e.meaning = m
#     e.save()


def main():
    os.system("createdb ActiveTeaching --owner postgres")
    os.system("python3 manage.py makemigrations")
    os.system("python3 manage.py migrate")
    fill_kanji_table()
    User.objects.create_superuser(f'{EMAIL_HOST_USER}',
                                  f'{EMAIL_HOST_PASSWORD}')


if __name__ == "__main__":
    main()
