from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, default=None)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, unique=True, default=None)
    designation = models.CharField(max_length=25, default=None)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
