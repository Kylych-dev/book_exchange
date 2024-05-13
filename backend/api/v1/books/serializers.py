from rest_framework import serializers
from apps.books.models import Book

class BookSerializer(serializers.ModelSerializer):
    # Устанавливаем поле owner только для чтения
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "public_date",
            "page",
            "author",
            "genre",
            "rating",
            "image",
            "owner",
            "isbn",
        )
        extra_kwargs = {
            "isbn": {"required": True},  # Делаем поле isbn обязательным
            "image": {"required": False},  # Делаем поле image необязательным
            # "owner": {"required": True}
        }

