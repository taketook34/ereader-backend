import os
import ebooklib
from bs4 import BeautifulSoup
from django.forms import model_to_dict
from ebooklib import epub

from rest_framework.response import Response
from .models import *
from rest_framework import generics

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

        obj = Book.objects.get(pk=serializer.data["id"])
        print(serializer.validated_data['book_src'].file)
        book = epub.read_epub(f"./{serializer.data['book_src']}")
        if book.get_metadata('DC', 'title'):
            obj.title = book.get_metadata('DC', 'title')[0][0]
            serializer.validated_data['title'] = book.get_metadata('DC', 'title')[0][0]

        if book.get_metadata('DC', 'creator'):
            obj.author = book.get_metadata('DC', 'creator')[0][0]
            serializer.validated_data['author'] = book.get_metadata('DC', 'creator')[0][0]

        if book.get_metadata('DC', 'description'):
            soup = BeautifulSoup(book.get_metadata('DC', 'description')[0][0], 'html.parser')
            obj.description = soup.text
            serializer.validated_data['description'] = soup.text
        obj.folder_src = serializer.data['book_src'][8:-5]
        obj.save()
        #serializer.data['title'] = 'Hello world!'
        os.system(f"unzip -o ./{serializer.data['book_src']} -d .{serializer.data['book_src'].replace(' ', '_')[:-5]}")
        print(obj.folder_src)

        return Response({'books': BookSerializer(obj).data})


class BookAPIDetailView(generics.RetrieveUpdateDestroyAPIView, generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIDestroy(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)

        if not pk:
            return Response({"post":"Please type id"})

        try:
            b = Book.objects.get(pk=pk)
        except:
            return Response({"post":"We do not have this id"})
        else:
            os.system(f"rm ./assets/{b.book_src}")
            os.system(f"rm -r ./assets/{b.folder_src}")
            b.delete()


        return Response({"post":"deleted post" + str(pk)})



