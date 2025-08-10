from rest_framework import serializers
from datetime import datetime, date
from .models import Book
from .models import Author


# A  BookSerializer that serializes all fields of the Book model.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Serialize all fields

    
    def validate(self, data):
        current_year = date.today().year
        if data['publication_year'] > current_year:
            raise serializers.ValidationError(
                {"publication_year": "Publication year cannot be in the future."}
            )
        return data

# An AuthorSerializer that includes:The name field.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for related books

    class Meta:
        model = Author
        fields = ['name', 'books']

