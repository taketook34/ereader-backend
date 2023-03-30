from rest_framework import serializers
from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "book_tags", "book_src", "cover_src", "folder_src", "time_update")

class BookAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "book_src")





