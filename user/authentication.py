from django.contrib.auth import authenticate
from tools.utils import Atomic

from django.core.mail import send_mail
from django.conf import settings

from user.models import Question, User
from teacher.models import Leitner


def login(r):

    user = authenticate(email=r.email, password=r.password)
    if user is not None:
    # A backend authenticated the credentials
        return None
    else:
        # No backend authenticated the credentials
        return user.learner


def sign_up(r, n_item):

    """
        Creates a new user and returns its id
    """

    leitner_teacher = Leitner.objects.create(n_item=n_item)
    u = User.objects.create_user(
        email=r.email,
        password=r.password,
        gender=r.gender,
        # leitner_teacher=leitner_teacher
    )

    return u.id


def email():
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    # return redirect('redirect to a new page')
