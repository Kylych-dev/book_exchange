from rest_framework import serializers
from apps.accounts.models import CustomUser
from .github_outh import GitHubOauth
from .helpers import register_social_user


class GitHubSocialAuthSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, code):
        access_token = GitHubOauth.exchange_code_for_token(code)

        if access_token:
            user_data = GitHubOauth.get_github_user(access_token)

            full_name = user_data['name']
            email = user_data['email']
            names = full_name.split(' ')
            first_name = names[1]
            last_name = names[0]
            provider = 'github'
        return register_social_user(
            provider,
            email,
            first_name,
            last_name
        )


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        # model = User
        fields = (
            # "phone_number",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            # "role",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    # def validate(self, attrs):
    #     if attrs.get('phone_number'):
    #         attrs['phone_number'] = normalize_phone_number(attrs['phone_number'])
    #     if attrs["password"] != attrs["password2"]:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."}
    #         )

    #     return attrs



'''
register

{
    "email": "user1@mail.ru",
    "first_name": "user1",
    "last_name": "user1",
    "password": "qwerty_1993",
    "password2": "qwerty_1993"
}



login
{
    "email": "user1@mail.ru",
    "password": "qwerty_1993"
}

'''