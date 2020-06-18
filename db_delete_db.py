import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from utils.console import AskUser

from ActiveTeachingServer.settings import DATABASES


DB_NAME = DATABASES['default']['NAME']


@AskUser
def delete_db():
    os.system(f'dropdb {DB_NAME}')
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
    os.system('find . -path "*/migrations/*.pyc" -delete')


if __name__ == "__main__":
    delete_db()
