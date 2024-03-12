from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CustomUserSerializer
# from api.auth.verify import twilio_send, twilio_check
# from apps.accounts.forms import VerifyForm
from apps.accounts.models import CustomUser
# from utils.phone_normalize import normalize_phone_number
from utils.customer_logger import logger




class RegisterView(viewsets.ViewSet):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        operation_description="Создание нового пользователя.",
        operation_summary="Создание нового пользователя",
        operation_id="register_user",
        tags=["Регистрация(register)"],
        responses={
            201: openapi.Response(description="OK - Регистрация прошла успешно."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def register(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                validated_data = serializer.validated_data
                print('validated data ----------->', serializer.validated_data)
                validated_data.pop("password2")
                # user_w = (
                    # None
                    # if request.user.is_anonymous
                    # else request.user.sewing_workshop_id
                #     **validated_data,
                # )
                user = CustomUser(
                    # sewing_workshop_id=user_w,
                    **validated_data,
                )
                user.set_password(validated_data.get("password"))
                user.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                    )

            except Exception as ex:
                logger.error(
                    f"Клиент не найден",
                    extra={
                        "Exception": ex,
                        "Class": f"{self.__class__.__name__}.{self.action}",
                    },
                )
                return Response(
                    data={"error": f"User creation failed: {str(ex)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )





class UserAuthenticationView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Авторизация пользователя для получения токена.",
        operation_summary="Авторизация пользователя для получения токена",
        operation_id="login_user",
        tags=["Вход(login)"],
        responses={
            200: openapi.Response(
                description="OK - Авторизация пользователя прошла успешно."
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    def login(self, request):
        print(request.data, '/*/*/*/*/*/*')
        phone_number = request.data["email"]
        password = request.data["password"]

        try:
            # phone_number = normalize_phone_number(phone_number)
            # user = CustomUser.objects.get(phone_number=phone_number)
            user = CustomUser.objects.get(email=phone_number)


        except CustomUser.DoesNotExist:
            print('hello')
            raise AuthenticationFailed("Такого пользователя не существует")

        if user is None:
            raise AuthenticationFailed("Такого пользователя не существует")

        # if not user.check_password(password):
        #     raise AuthenticationFailed("Не правильный пароль")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        print('ok')
        return Response(
            data={
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Выход для удаления токена.",
        operation_summary="Выход для удаления токена",
        operation_id="logout_user",
        tags=["Выход(logout)"],
        responses={
            201: openapi.Response(
                description="OK - Выход пользователя прошла успешно."
            ),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def logout(self, request):
        try:
            if "refresh_token" in request.data:
                refresh_token = request.data["refresh_token"]
                if refresh_token:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                return Response("Вы вышли из учетной записи", status=status.HTTP_200_OK)
            else:
                return Response(
                    "Отсутствует refresh_token", status=status.HTTP_400_BAD_REQUEST
                )
        except TokenError:
            raise AuthenticationFailed("Не правильный токен")



"""
127.0.0.1:3000/api/v1/login/?access_token=ваш_access_token


register postman 

{
    "email": "ww1@mail.ru",
    "password": "mirbekov 1993",
    "password2": "mirbekov 1993",
    "first_name": "bob",
    "last_name": "malkovich"
}




{
    "phone_number": "+996701390149",
    "password": "mirbekov 1993",
    "password2": "mirbekov 1993",
    "first_name": "field",
    "last_name": "required"
}



ok 201

{
    "email": "ww@mail.ru",
    "password": "mirbekov 1993",
    "password2": "mirbekov 1993",
    "first_name": "field",
    "last_name": "required"
}


login

{
    "email": "ww@mail.ru",
    "password": "mirbekov 1993"
}



{
    "email": "qw@mail.ru",
    "password": "mirbekov 1993"
}





{
    "title": "qwerty",
    "description": "книга",
    "public_date": "2023-01-15",
    "page": 800,
    "author": 1, 
    "genre": 1, 
    "rating": 4.5,
}



"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NDMzNTEyLCJpYXQiOjE3MDg0MzMyMTIsImp0aSI6ImUxZmUzOWM3YzFhNzQ2MmNiMGRhMGU3YzRkMjA0NDZiIiwidXNlcl9pZCI6Mn0.bsNhJht2UYjuLDBsSMxAsKxwvThquxbi-oLz4B_R_Yc",
"refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwODUxOTYxMiwiaWF0IjoxNzA4NDMzMjEyLCJqdGkiOiIwYjRlMzkxNGNhNTA0ZGIyOTdjNzZkNDkxNGIxODk0ZCIsInVzZXJfaWQiOjJ9.ljEIaaYSgo0n0dPe0K9mqeHHtUvOXuSWuTfL8fQbXeM"}







http://127.0.0.1:3000/api/v1/book/?bearer_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NTM1NTY0LCJpYXQiOjE3MDg1MzE5NjQsImp0aSI6ImJkMGU4NmY2MDk2OTRiZTg5ZTcxM2ViOTkwNjRmOWU1IiwidXNlcl9pZCI6Mn0.ORIf14p_ssV2u-tOFQbWyUoWL-x1nJjsIbQvcRS7PO4


"""