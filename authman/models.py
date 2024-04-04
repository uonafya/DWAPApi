from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from django.contrib.auth.models import Group
from api.models import *


class RoleScreens(models.Model):
    role_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    screens = models.TextField(
        max_length=2500, default="Dashboard,DataAlignment,IndicatorMappingRules,IndicatorComparison,DataQuality,Indicators,AllIndicators,Categories,Security,DataPullSchedule,Roles,Users,PasswordPolicy,Reports")
    counties = models.ManyToManyField(counties)
    facilities = models.ManyToManyField(Facilities)

    class Meta:
        db_table = 'role_screens'
        verbose_name_plural = 'Role Access'

    def __str__(self) -> str:
        return self.role_id.name + " metadata"

class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        """
        Creates and saves a User with the given email, phone and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, phone, password=password, **extra_fields)

class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=100,
        unique=True,
    )
    phone = models.CharField(max_length=15)
    organisation = models.CharField(
        max_length=255, default='HealthIT', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'first_name',
                       'last_name', 'email']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Hash the password before saving the user
        super().save(*args, **kwargs)
