import os

from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from ereader.settings import BASE_DIR
from .models import *
from rest_framework import generics, viewsets

from .serializers import BookSerializer




class BookAPIList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAPICreate(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #print(request.data['book_src'])
        serializer.save()
        #print(serializer.data['book_src'])
        os.system("ls -l assets/books")
        os.system(f"unzip -o ./{serializer.data['book_src']} -d ./assets/books/{serializer.data['title'].replace(' ', '_')}")


        return Response({'book': serializer.data})

class BookAPIDetailView(generics.RetrieveUpdateDestroyAPIView, generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIDestroy(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



