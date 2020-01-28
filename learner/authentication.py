from django.contrib.auth import authenticate
from tools.utils import Atomic

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from learner.models import Question, User
from teacher.models import Leitner


def login(r):
    # Return User object if a backend authenticated the credentials,
    # None otherwise
    return authenticate(email=r.email, password=r.password)


def sign_up(r):

    """
        Creates a new learner and returns its id
    """

    try:
        user = User.objects.create_user(
            email=r.email,
            password=r.password,
            gender=r.gender,
            mother_tongue=r.mother_tongue
        )

    except IntegrityError:
        return None

    return user


def email(email_address):
    subject = 'Thank you for registering to our site'
    message = 'It  means a world to us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address, ]
    send_mail(subject, message, email_from, recipient_list)
    # return redirect('redirect to a new page')
