import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import Parameter, PredefinedQuestion

from utils import AskUser
from create_predefined_question import create_predefined_questions


N_KANJI = 20


@AskUser
def prepare_xp():

    # Turn off test mode
    p_test = Parameter.objects.get(name='test')
    p_test.value = 0
    p_test.save()

    print('Test Mode: OFF')

    # Check everything is in order with predefined questions
    p_use_predefined = Parameter.objects.get(name='use_predefined_question')
    print(f'Predefined Questions: {"ON" if p_use_predefined.value==1 else "OFF"}')
    if p_use_predefined.value == 1:

        t_max = Parameter.objects.get(name='t_max').value

        if len(PredefinedQuestion.objects.all()) != t_max:
            print(f"Creating predefined questions with {N_KANJI} different kanji for {t_max} time steps...")
            create_predefined_questions(n_kanji=N_KANJI)

        print(f"Predefined questions with {N_KANJI} different kanji for {t_max} time steps will be used.")


if __name__ == "__main__":

    prepare_xp()
