from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The Email must be set'))
        uname = self.normalize_email(username)
        user = self.model(username=uname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    GEEKS_CHOICES = (
        ("Admin", "Admin"),
        ("Store", "Store"),
        ("Inventory", "Inventory"),
        ("Production", "Production"),
        ("Quality Control", "Quality Control"),
        ("QC_Analyst", "QC_Analyst"),
        ("Quality Assurance", "Quality Assurance"),
        ("RD", "RD"),
    )
    username = models.CharField(max_length=255, verbose_name='username', unique=True)
    #image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    role = models.CharField(max_length=255, choices=GEEKS_CHOICES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.id}: {self.username}'