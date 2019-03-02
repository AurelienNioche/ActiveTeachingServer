import os

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Your application specific imports
from task.models import Kanjilist


def has_numbers(string):

    return any(char.isdigit() for char in string)

def extract_single_meaning(meanings):

    m = meanings.split(";")[0].split(",")[0].split('(')[0]

    if not has_numbers(m):
        m = m.split('.')[0]

    if m == "A":
        m = "first"
    elif m == "B":
        a = "second"

    else "second"

def main():

    for e in Kanjilist.objects.all():

        k = e.kanji
        km = e.translation_of_kun
        om = e.translation_of_on

        # if km == '-':

        print(k)
        print(extract_single_meaning(km))
        print(km)
        print()
        print(extract_single_meaning(om))
        print(om)
        print("*" * 10)

if __name__ == "__main__":

    main()
