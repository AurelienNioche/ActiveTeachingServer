import os
import sys

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import User, Question


class AskUser:

    def __init__(self, f):
        self.f = f

    def __call__(self):

        while True:
            r = input("Are you sure you want to operate this change?")
            r.lower()
            if r == 'n':
                sys.exit()
            elif r == 'y':
                break
            else:
                print("Your response have to be 'y' or 'n'!")
        self.f()
        print("Done!")


@AskUser
def main():

    User.objects.all().delete()
    Question.objects.all().delete()


if __name__ == "__main__":
    main()
