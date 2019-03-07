import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import User, Question


from datetime import datetime, timedelta


def main():

    user_id = 244179
    que = Question.objects.filter(user_id=user_id).order_by('t')

    for q in que:

        print(q.reply, q.correct_answer, int((q.time_reply - q.time_display).total_seconds()*10**3))


if __name__ == "__main__":

    main()
