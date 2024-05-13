from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where membership_number is the unique identifiers
    for authentication.
    """
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
        extra_fields.setdefault("is_verified", True)
        return self.create_user(email, password, **extra_fields)

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
