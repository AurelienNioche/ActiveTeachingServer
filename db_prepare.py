import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# from teaching_material.db_operation import fill_kanji_table
# #
# #
# # fill_kanji_table()
from teaching_material.models import Kanji, Meaning

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

def backup_table(model):
    command = \
        f'pg_dump -Fc --column-inserts --data-only ' \
        f'--table {model._meta.db_table} ' \
        f'{DB_NAME} ' \
        f'> data/{model.__name__}.dump'

    print(f"Run command '{command}'")
    os.system(command)


def main():

    backup_table(Kanji)
    backup_table(Meaning)


if __name__ == "__main__":
    main()
