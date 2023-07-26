from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    '''Менеджер для создания пользователей'''

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Создать и сохранить user эл почтой и паролем'''
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('Password is not provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        '''Создать и сохранить обычного user с данной почтой и паролем'''
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''Создать и сохранить SuperUser c почтой и паролем'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

