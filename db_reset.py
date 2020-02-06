import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import os

from tools.utils import AskUser


@AskUser
def reset():

    os.system("dropdb ActiveTeaching")
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')


if __name__ == "__main__":

    reset()
