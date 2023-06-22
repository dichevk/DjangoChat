import uuid 

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

class ChatUserManager(UserManager):
    def create_user(self, name, email, password):
        email = self.normalize_email(email=email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using= self.db)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField
    email = models.EmailField(unique=True)
    name = models.CharField(default='')
    role = models.CharField()

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    last_login_at = models.DateTimeField(blank=True, null=True)

    objects = ChatUserManager()