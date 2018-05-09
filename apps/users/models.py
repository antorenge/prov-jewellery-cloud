"""
Users models
"""
from sorl.thumbnail import ImageField
from django.db import models
from django.core import validators
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    """
    Manages creation of user accounts
    """

    def _create_user(self, email, password, **extra_fields):
        """ Creates user given email and password """
        if not email:
            raise ValueError('Users must have a valid email address.')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates standard user account without any privileges"""
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Creates user account with superuser privileges """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    first_name = models.CharField('first name', max_length=24, blank=True)
    last_name = models.CharField('last name', max_length=24, blank=True)
    gender = models.CharField('gender', max_length=6, blank=True,
                              choices=(('male', 'Male'), ('female', 'Female')))
    email = models.EmailField('email address', unique=True)
    phone = models.CharField('phone number', max_length=15, unique=True)
    picture = ImageField(upload_to='pictures/%Y/%m',
                         default='pictures/default.png')
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('status', default=True)
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
