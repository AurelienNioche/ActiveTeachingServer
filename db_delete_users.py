import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from learner.models import User
from utils.console import AskUser


@AskUser
def delete_users():
    users = User.objects.all()

    for u in users:
        if u.is_superuser is False:
            u.delete()


if __name__ == "__main__":
    delete_users()
