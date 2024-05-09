from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(
        help_text='Enter a valid phone number like +12125552368',
        null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    has_default_password = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    class Meta:
        verbose_name = 'user'

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def short_name(self):
        return self.first_name

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(
        'Account', on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default_profile_pic.png',
        blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.user.full_name}'

    @property
    def avatar(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None


class Role(Group):
    class Meta:
        proxy = True
