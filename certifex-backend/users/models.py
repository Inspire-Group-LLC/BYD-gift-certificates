from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_superuser=False, **extra_fields):
        user = self.model(username=username, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with an encrypted password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, is_superuser=True, **extra_fields)

class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True, default='')
    phone_number = models.CharField(max_length=15)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True, default='password')
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    # Add unique related_name for groups and user_permissions
    groups = models.ManyToManyField(
        Permission,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_permissions',
        related_query_name='user',
    )

    def __str__(self):
        return self.full_name
