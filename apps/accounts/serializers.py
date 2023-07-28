
from .models import UserModel
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation
from django.contrib.auth.models import BaseUserManager

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'auth_token')
        read_only_fields = ('is_active', 'is_staff')

    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number')

    # def validate_email(self, value):
    #     user = UserModel.objects.filter(email=value)
    #     if user:
    #         raise serializers.ValidationError('Email is already taken')
    #     return BaseUserManager.normilize_email(value)

    def validate_email(self, data):

        if hasattr(data, 'get'):
            print(data.get('email'), '***************')
        else:
            print('Value is not a dict', '***************')

        print('------>', data, type(data))

        email = data.get('email')
        phonenumber = data.get('phone_number')

        if not email and not phonenumber:
            raise serializers.ValidationError('one of email or phone number required')
        return data

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name')
        # fields = '__all__'
        read_only_fields = ('email',)

class EmptySerializer(serializers.Serializer):
    pass


