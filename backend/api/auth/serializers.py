from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.accounts.models import CustomUser
# from django.contrib.auth import get_user_model
# from utils.phone_normalize import normalize_phone_number


# User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    # phone_number = serializers.CharField(required=True)
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

