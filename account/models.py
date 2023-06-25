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
        
        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    REGULAR = 'regular'
    MANAGER = 'manager'

    ROLES_CHOICES = (
        (REGULAR, 'Regular'),
        (MANAGER, 'Manager'),
    )

    id = models.UUIDField
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, default='')
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, )

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    last_login_at = models.DateTimeField(blank=True, null=True)

    objects = ChatUserManager()