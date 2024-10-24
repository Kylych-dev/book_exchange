from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from query_counter.decorators import queries_counter


from apps.books.models import (
    Author,
    Genre
)

from .serializers import (
    AuthorSerializer,
    GenreSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @queries_counter
    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        queryset = self.get_queryset().prefetch_related('books')
        # serializer = self.serializer_class(self.get_queryset(), many=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]

    @queries_counter
    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)