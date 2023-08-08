
from . import models
from . import serializers
from rest_framework.views import APIView
# from rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import RegisterView
# from requests import Response
from rest_framework.response import Response
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from apps.utils.authenticate_user import get_and_authenticate_user
from django.contrib.auth import logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {'login': serializers.UserLoginSerializer,
                          'register': serializers.UserRegisterSerializer,
                          'password_change': serializers.PasswordChangeSerializer}

    @action(methods=['POST',], detail=False)
    def login(self, request):
        print('hello I\'m here')
        serializer = self.get_serializer(data=request.data)
        print('hello I\'m here 2')
        serializer.is_valid(raise_exception=True)
        print('hello I\'m here 3')
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        response = serializer.get_jwt_token(serializer.data)

        return Response(response)
        user = get_and_authenticate_user(**serializer.validated_data)


        data = serializers.AuthUserSerializer(user).data

        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):


        # print(request, '------THIS IS REQUEST------')
        # print(request.data, '------THIS IS REQUEST------')
        # for i in request.data.items():
        #     print(i)

        serializer = self.get_serializer(data=request.data)
        print(serializer, '<------- THIS is SERIALIZER')
        serializer.is_valid(raise_exception=True)
        print('\\\\\\\\\\\\')
        print(**serializer.validated_data)

        user = self.perform_create(**serializer.validated_data)
        print(user, 'THIS IS serializer')
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def perform_create(self, data):
        user_manager = models.CustomUserManager()
        # email = data.validated_data['email']
        # password = data.validated_data['password']
        email = data.get('email')
        password = data.get('password')
        user = user_manager.create_user(email=email, password=password)
        return user

    @action(methods=['POST',], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return None


    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict mapping.')

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()






class CustomRegisterView(RegisterView):
    queryset = models.UserModel.objects.all()

class UserAPIView(APIView):
    @staticmethod
    def get(request):
        users = models.UserModel.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
