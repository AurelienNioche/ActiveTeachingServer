from django.contrib.auth import authenticate

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from learner.models.user import User


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
        if condition == User.Condition.TEST:
            user = User.objects.create_user(
                email=email,
                password=password,
                gender=gender,
                mother_tongue=mother_tongue,
                other_language=other_language,
                age=age,
                condition=condition
            )
            from teacher.models.leitner import Leitner
            from teacher.models.threshold import Threshold
            from teaching_material.models import Kanji
            material = Kanji.objects.all()
            Leitner.objects.create(user=user,
                                   material=material[0:50],
                                   delay_factor=2)
            Threshold.objects.create(user=user,
                                     material=material[50:100],
                                     learnt_threshold=0.90,
                                     heterogeneous_param=False,
                                     bounds=((0.001, 0.04), (0.2, 0.5)),
                                     grid_size=20)

        else:
            raise ValueError

    except IntegrityError as e:
        raise e

    return user


def send_email(email_address):
    subject = 'Thank you for registering to our site'
    message = 'It  means a world to us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address, ]
    send_mail(subject, message, email_from, recipient_list)
