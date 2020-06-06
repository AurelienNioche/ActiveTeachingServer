from django.contrib.auth import authenticate
# from tools.utils import Atomic

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from learner.models import User
# from teacher.models import Leitner


def login(email, password):
    # Return User object if a backend authenticated the credentials,
    # None otherwise
    return authenticate(email=email, password=password)


def sign_up(email, password, gender, age,
            mother_tongue, other_language, condition):

    """
        Creates a new learner and returns its id
    """

    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            gender=gender,
            mother_tongue=mother_tongue,
            other_language=other_language,
            age=age,
            condition=condition
        )

    except IntegrityError:
        return None

    return user


def send_email(email_address):
    subject = 'Thank you for registering to our site'
    message = 'It  means a world to us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address, ]
    send_mail(subject, message, email_from, recipient_list)
    # return redirect('redirect to a new page')
