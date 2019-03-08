import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import User, Question

from utils import AskUser


@AskUser
def main():

    User.objects.all().delete()
    Question.objects.all().delete()


if __name__ == "__main__":
    main()
