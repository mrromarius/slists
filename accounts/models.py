import email
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class Token(models.Model):
    '''маркер'''
    email = models.EmailField()
    uid = models.CharField(max_length=255)

class ListUSer(AbstractBaseUser, PermissionsMixin):
    '''пользователь списка'''
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email', 'height']

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == 'Romashev.Al.s@gmail.com'

    @property
    def is_active(self):
        return True
