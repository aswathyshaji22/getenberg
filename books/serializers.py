from rest_framework import serializers
from .models import Author, Subject, Bookshelf, Format, Book

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes name, birth year, and death year.
    """
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    """
    class Meta:
        model = Subject
        fields = ['name']


class BookshelfSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bookshelf model.
    """
    class Meta:
        model = Bookshelf
        fields = ['name']


class FormatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Format model.
    Includes MIME type and download URL.
    """
    class Meta:
        model = Format
        fields = ['mime_type', 'url']


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Nested serializers are used for author, subjects, bookshelves, and formats.
    """
    author = AuthorSerializer()
    subjects = SubjectSerializer(many=True)
    bookshelves = BookshelfSerializer(many=True)
    formats = FormatSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'title',
            'gutenberg_id',
            'language',
            'downloads',
            'author',
            'subjects',
            'bookshelves',
            'formats'
        ]
