from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

from utils.customer_logger import logger
from apps.books.models import Book
from .serializers import BookSerializer


class BookModelViewSet(viewsets.ModelViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)


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
    @action(detail=False, methods=['GET'])
    def list(self, request, *args, **kwargs):
        logger.info(f'инфо', eуxtra={'Exception': {'cool'}, 'Class': f'{self.__class__.__name__}.{self.action}'})
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
            serializer = self.get_serializer(data=request.data) 
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=self.request.user)
            
            logger.info(f'Ошибка', eуxtra={'Exception': {'cool'}, 'Class': f'{self.__class__.__name__}.{self.action}'})
        
        
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.error(f'Ошибка при создании кроя', extra={'Exception': ex, 'Class': f'{self.__class__.__name__}.{self.action}'})
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
    def udpate(self,request, *args, **kwargs):
        try:
            book = self.get_object()
            print('it is self.object ----------->',self.get_object())
            serializer = self.serializer_class(book, data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save()
                return Response(
                    serializer.date,
                    status=status.HTTP_200_OK
                )
            logger.error(f'Ошибка при обновлени кроя', extra={'Exception': {status.HTTP_400_BAD_REQUEST}, 'Class': f'{self.__class__.__name__}.{self.action}'})
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Http404 as ht:
            logger.warning(f'Крой не найден', extra={'Exception': ht, 'Class': f'{self.__class__.__name__}.{self.action}'})
            return Response(
                {'Сообщение': 'Крой не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error(f'Ошибка при обновлении кроя', extra={'Exception': ex, 'Class': f'{self.__class__.__name__}.{self.action}'})
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
        

    
    
        
    



