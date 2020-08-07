import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from ActiveTeachingServer.settings import DATABASES


DB_NAME = DATABASES['default']['NAME']

os.system(f"createdb {DB_NAME} --owner postgres")
os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")
