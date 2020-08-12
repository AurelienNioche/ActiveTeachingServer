from django.contrib.auth import authenticate

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from user.models.user import User


def login(email, password):
    # Return User object if a backend authenticated the credentials,
    # None otherwise
    return authenticate(email=email, password=password)


def sign_up(email, password, gender, age,
            mother_tongue, other_language, condition, *args, **kwargs):

    """
        Creates a new learner and returns its id
    """

    try:
        u = User.objects.create_user(
            email=email,
            password=password,
            gender=gender,
            mother_tongue=mother_tongue,
            other_language=other_language,
            age=age,
            condition=condition)
        from experimental_condition import experimental_condition
        experimental_condition.user_creation(user=u, *args, **kwargs)

    except IntegrityError as e:
        raise e

    return u


def send_email(email_address):
    subject = 'Thank you for registering to our site'
    message = 'It  means a world to us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address, ]
    send_mail(subject, message, email_from, recipient_list)
