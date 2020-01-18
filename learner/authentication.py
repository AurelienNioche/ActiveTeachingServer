from django.contrib.auth import authenticate
from tools.utils import Atomic

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from learner.models import Question, User
from teacher.models import Leitner


def login(r):

    u = authenticate(email=r.email, password=r.password)
    if u is None:
        # No backend authenticated the credentials
        print("Authentication failed")
        return -1
    else:
        # A backend authenticated the credentials
        print(f"User {u.id}: Authentication succeed")
        return u.id


def sign_up(r, n_item):

    """
        Creates a new learner and returns its id
    """

    try:
        u = User.objects.create_user(
            email=r.email,
            password=r.password,
            gender=r.gender,
            mother_tongue=r.mother_tongue
        )
        Leitner.objects.create(user=u, n_item=n_item)

    except IntegrityError:
        return -1

    return u.id


def email():
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    # return redirect('redirect to a new page')
