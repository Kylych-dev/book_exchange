from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from utils.customer_logger import log_error, log_warning
from apps.books.models import Book
from apps.accounts.models import CustomUser
from .serializers import BookSerializer


'''
log_error(self, ex)
log_warning(self, ex)
'''


class BookModelViewSet(viewsets.ModelViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # template_name = 'books/book_list.html'

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(owner=user)

    @swagger_auto_schema(
        method='get',
        operation_description='Список книг',
        operation_id='list_books',
        operation_summary='Список книг',
        tags=['Book'],
        responses={
            200: openapi.Response(description='OK'),
            400: openapi.Response(description='Bad Request'),
        },
    )
    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        operation_description='Создание нового элемента книги',
        operation_summary='Создание элемента книги',
        operation_id='create_book',
        tags=['Book'],
        responses={
            201: openapi.Response(description='Created - Элемент успешно создан'),
            400: openapi.Response(description='Bad Request - Неверный запрос'),
        },
    )
    @action(detail=True, methods=['POST'])
    def create(self, request, *args, **kwargs):
        try:
            isbn = request.data.get('isbn')
            if Book.objects.filter(isbn=isbn).exists():
                log_error(self, 'Книга с таким ISBN уже существует сообщение Лог')
                return Response(
                    {'message': 'Книга с таким ISBN уже существует ++++'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=request.data) 
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=self.request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as ex:
            log_error(ex)
            return Response(
                {'Сообщение': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @swagger_auto_schema(
        method='put',
        operation_description='Обновление данных элемента книги',
        operation_summary='Обновление элемента книги',
        operation_id='update_book',
        tags=['Book'],
        responses={
            200: openapi.Response(description='OK - Элемент успешно обновлен'),
            400: openapi.Response(description='Bad Request - Неверный запрос'),
            404: openapi.Response(description='Not Found - Ресурс не найден'),
        },
    )
    @action(detail=True, methods=['PUT'])
    def udpate(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            print('it is self.object ----------->', self.get_object())
            serializer = self.serializer_class(book, data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save()
                return Response(
                    serializer.date,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Http404 as ht:
            log_warning(self, ht)
            return Response(
                {'Сообщение': 'Крой не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
           # log
            return Response(
                {'Сообщение': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @swagger_auto_schema(
        method='delete',
        operation_description='Удаление элемента книги',
        operation_summary='Удаление элемента книги',
        operation_id='delete_book',
        tags=['Book'],
        responses={
            204: openapi.Response(description='No Content - Элемент успешно удален'),
            404: openapi.Response(description='Not Found - Ресурс не найден'),
            403: openapi.Response(description='Forbidden - Недостаточно прав'),
        },
    )
    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {"message": "Ресурс не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        method='post',
        operation_description='Передача книги',
        operation_summary='Передача книги',
        operation_id='share_book',
        tags=['Book'],
        responses={
            200: openapi.Response(description='OK - Данные успешно получены'),
            404: openapi.Response(description='Not Found - Ресурс не найден'),
        },
    )
    @action(detail=True, methods=['POST'])
    def transfer(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            new_owner_id = request.data.get('new_owner_id')

            if new_owner_id is None:
                return Response(
                    {'message': 'Не указан новый владелец'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                print('new_owner_id ----------->', new_owner_id)
                new_owner = CustomUser.objects.filter(id=new_owner_id).first()
            except CustomUser.DoesNotExist:
                raise Http404('Пользователь не найден')

            instance.owner = new_owner
            instance.save()

            return Response(
                {"message": "Книга успешно передана"},
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                {"message": "Ресурс не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
    



