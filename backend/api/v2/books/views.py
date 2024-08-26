from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    status,
    permissions,
    generics
)

from django.http import Http404

from apps.accounts.models import CustomUser
from .serializers import BookSerializer
from apps.books.models import (
    Book,
    Author
)
from utils.customer_logger import (
    log_error,
    log_warning
)


'''
log_error(self, ex)
log_warning(self, ex)
'''


class BookModelViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(user, '---------')
        if user.is_staff:
            return Book.objects.all()
        return Book.objects.filter(owner=user)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

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
            # log_error(ex)
            return Response(
                {'Сообщение': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
)

    @action(detail=True, methods=['PUT'])
    def udpate(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            serializer = self.serializer_class(book, data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save()
                return Response(
                    serializer.date,
                    status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        except Http404 as ht:
            log_warning(self, ht)
            return Response(
                {'Сообщение': 'Крой не найден'},
                status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
           # log
            return Response(
                {'Сообщение': str(ex)},
                status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {"message": "Ресурс не найден"},
                status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['POST'])
    def transfer(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            new_owner_id = request.data.get('new_owner_id')

            if new_owner_id is None:
                return Response(
                    {'message': 'Не указан новый владелец'},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                new_owner = CustomUser.objects.filter(id=new_owner_id).first()
            except CustomUser.DoesNotExist:
                raise Http404('Пользователь не найден')
            instance.owner = new_owner
            instance.save()
            return Response(
                {"message": "Книга успешно передана"},
                status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"message": "Ресурс не найден"},
                status=status.HTTP_404_NOT_FOUND)
    

class BooksByAuthorView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        # author_name = self.request.query_params.get('author_name')
        print('---------')
        author_id = self.kwargs['author_id']
        return Book.objects.filter(author_id=author_id)

