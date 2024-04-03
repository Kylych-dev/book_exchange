from rest_framework import serializers
from apps.accounts.models import CustomUser



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

