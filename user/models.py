from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.utils.timezone import now

import numpy as np
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from teacher.models import Leitner


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Question(models.Model):

    user_id = models.IntegerField(default=-1)
    t = models.IntegerField(default=-1)
    question = models.IntegerField(default=-1)
    possible_replies = ArrayField(models.IntegerField(), default=list)
    reply = models.IntegerField(default=-1)
    success = models.BooleanField()
    time_display = models.DateTimeField(default=now)
    time_reply = models.DateTimeField(default=now)

    class Meta:

        db_table = 'question'
        app_label = 'user'


class User(AbstractUser):

    # Change manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # changes email to unique and blank to false
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

    gender = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    mother_tongue = models.TextField(blank=True, null=True)
    other_language = models.TextField(blank=True, null=True)
    registration_time = models.DateTimeField(default=now)

    leitner_teacher = models.OneToOneField(Leitner, on_delete=models.CASCADE,
                                           null=True, blank=True)

    class Meta:
        db_table = 'user'
        app_label = 'user'
