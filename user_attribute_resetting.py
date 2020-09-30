import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user.models.user import User


def main():
    while True:
        try:
            email = input("email:")
            user = User.objects.get(email=email)
            break
        except Exception as e:
            print(f"encountered error '{e}', please retry!")

    new_password = input("new password:")

    ready = input("confirm the change (enter 'yes' or 'y' to continue)?")
    if ready not in ('y', 'yes'):
        print("Operation cancelled")
        exit(0)

    user.set_password(new_password)
    user.save()
    print("Done")


if __name__ == "__main__":
    main()
