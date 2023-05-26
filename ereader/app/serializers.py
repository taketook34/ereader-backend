from rest_framework import serializers
from .models import *
import os

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "book_src")

class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "book_src", "title", "author", "folder_src", "cover_src")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        b = Book.objects.get(id=data["id"])
        src_book = b.book_src.path
        data['book_src'] = src_book[src_book.find('/books'):]
        src_book  = b.folder_src.path
        data['folder_src'] = src_book[src_book.find('/books'):]
        if b.cover_src:
            src_book = b.cover_src.path
            data['cover_src'] = src_book[src_book.find('/books'):]
        return data

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "book_src", "title", "author", "folder_src", "cover_src")





