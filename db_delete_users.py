import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from learner.models.user import User
from utils.console import AskUser


@AskUser
def delete_users():
    User.objects.filter(is_superuser=False).delete()


if __name__ == "__main__":
    delete_users()
