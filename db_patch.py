import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user.models.user import User
# from user.models.session import Session
# from user.models.question import Question


def main():

    for u in User.objects.exclude(is_superuser=True):
        if 'test' not in u.email:
            u.experiment_name = "2020-09-04"
            u.save()


if __name__ == "__main__":
    main()
    print("Done!")
