from rest_framework import serializers

from api.v1.books.serializers import BookSerializer
from apps.books.models import (
    Author,
    Genre
)

class AuthorSerializer(serializers.ModelSerializer):
    # books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            # 'books'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

