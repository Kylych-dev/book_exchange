from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where membership_number is the unique identifiers
    for authentication.
    """

    # def create_user(self, email, password=None, **extra_fields):
    #     """
    #     Create and save a User with given membership_number and password.
    #     """
    #     user = self.model(
    #         email=email,
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     """
    #     Create and save a SuperUser with the given membership_number and password.
    #     """
    #     user = self.create_user(email, password, **extra_fields)
    #     user.is_superuser = True
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.save(using=self._db)
    #     return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=255, blank=True)
    last_name= models.CharField('Last Name', max_length=255, blank=True, null=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomUserManager() 
    
    USERNAME_FIELD = 'email'


    # REQUIRED_FIELDS = []

    
    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
