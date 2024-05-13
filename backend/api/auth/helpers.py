import requests
from apps.accounts.models import CustomUser
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, email, first_name, last_name):
    old_user = CustomUser.objects.filter(email=email).first()
    if old_user.exists():
        if provider == old_user[0].auth_provider:
            register_user = authenticate(email=email, password=settings.SOCIAL_SECRET)

            return {
                'email': register_user.email,
                'tokens': register_user.tokens()
            }
        else:
            raise AuthenticationFailed(
                'Please continue your login using ' + old_user[0].auth_provider
            )
    else:
        new_user = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': settings.SOCIAL_AUTH_PASSWORD,
            'is_active': True
        }
        user = CustomUser.objects.create_user(**new_user)
        user.auth_provider = provider
        user.is_verified = True
        user.save()
        login_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)

        tokens = login_user.tokens()

        return {
            'email': login_user.email,
            "full_name": f"{login_user.first_name} {login_user.last_name}",
            "access": str(tokens.get('access')),
            "refresh": str(tokens.get('refresh'))
        }

        # user = CustomUser(
        #     email=email,
        #     first_name=first_name,
        #     last_name=last_name,
        #     password=settings.SOCIAL_AUTH_PASSWORD,
        #     is_active=True
        # )
        # user.set_unusable_password()
        # user.save()
        # return {
        #     'email': user.email,
        #     'tokens': user.tokens()
        # }


'''
    email
    first_name
    last_name
'''

