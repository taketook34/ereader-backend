import os
import ebooklib
from bs4 import BeautifulSoup
from django.forms import model_to_dict
from ebooklib import epub

from rest_framework.response import Response
from .models import *
from rest_framework import generics

from .serializers import *
import zipfile
from lxml import etree
namespaces = {
    "calibre": "http://calibre.kovidgoyal.net/2009/metadata",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "opf": "http://www.idpf.org/2007/opf",
    "u": "urn:oasis:names:tc:opendocument:xmlns:container",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xhtml": "http://www.w3.org/1999/xhtml"
}

class BookAPIList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookViewSerializer


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
        print(serializer.data['book_src'])
        os.system("ls assets/books")
        cover = get_epub_cover(f"./{serializer.data['book_src']}")
        if cover:
            print(os.path.join(serializer.data['book_src'][8:-5], cover))
            obj.cover_src = os.path.join(serializer.data['book_src'][8:-5], cover)


        obj.save()

        os.system(f"unzip -o ./{serializer.data['book_src']} -d .{serializer.data['book_src'].replace(' ', '_')[:-5]}")
        return Response({'books': BookSerializer(obj).data})


class BookAPIDetailView(generics.RetrieveUpdateDestroyAPIView, generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookViewSerializer

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



def get_epub_cover(epub_path):
    ''' Return the cover image file from an epub archive. '''

    # We open the epub archive using zipfile.ZipFile():
    with zipfile.ZipFile(epub_path) as z:

        # We load "META-INF/container.xml" using lxml.etree.fromString():
        t = etree.fromstring(z.read("META-INF/container.xml"))
        # We use xpath() to find the attribute "full-path":
        '''
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf" ... />
          </rootfiles>
        </container>
        '''
        rootfile_path = t.xpath("/u:container/u:rootfiles/u:rootfile",
                                namespaces=namespaces)[0].get("full-path")
        print("Path of root file found: " + rootfile_path)

        # We load the "root" file, indicated by the "full_path" attribute of "META-INF/container.xml", using lxml.etree.fromString():
        t = etree.fromstring(z.read(rootfile_path))

        cover_href = None
        try:
            # For EPUB 2.0, we use xpath() to find a <meta>
            # named "cover" and get the attribute "content":
            '''
            <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
              ...
              <meta content="my-cover-image" name="cover"/>
              ...
            </metadata>            '''

            cover_id = t.xpath("//opf:metadata/opf:meta[@name='cover']",
                               namespaces=namespaces)[0].get("content")
            print("ID of cover image found: " + cover_id)
            # Next, we use xpath() to find the <item> (in <manifest>) with this id
            # and get the attribute "href":
            '''
            <manifest>
                ...
                <item id="my-cover-image" href="images/978.jpg" ... />
                ... 
            </manifest>
            '''
            cover_href = t.xpath("//opf:manifest/opf:item[@id='" + cover_id + "']",
                                 namespaces=namespaces)[0].get("href")
        except IndexError:
            pass

        if not cover_href:
            # For EPUB 3.0, We use xpath to find the <item> (in <manifest>) that
            # has properties='cover-image' and get the attribute "href":
            '''
            <manifest>
              ...
              <item href="images/cover.png" id="cover-img" media-type="image/png" properties="cover-image"/>
              ...
            </manifest>
            '''
            try:
                cover_href = t.xpath("//opf:manifest/opf:item[@properties='cover-image']",
                                     namespaces=namespaces)[0].get("href")
            except IndexError:
                pass

        if not cover_href:
            # Some EPUB files do not declare explicitly a cover image.
            # Instead, they use an "<img src=''>" inside the first xhmtl file.
            try:
                # The <spine> is a list that defines the linear reading order
                # of the content documents of the book. The first item in the
                # list is the first item in the book.
                '''
                <spine toc="ncx">
                  <itemref idref="cover"/>
                  <itemref idref="nav"/>
                  <itemref idref="s04"/>
                </spine>
                '''
                cover_page_id = t.xpath("//opf:spine/opf:itemref",
                                        namespaces=namespaces)[0].get("idref")
                # Next, we use xpath() to find the item (in manifest) with this id
                # and get the attribute "href":
                cover_page_href = t.xpath("//opf:manifest/opf:item[@id='" + cover_page_id + "']",
                                          namespaces=namespaces)[0].get("href")
                # In order to get the full path for the cover page,
                # we have to join rootfile_path and cover_page_href:
                cover_page_path = os.path.join(os.path.dirname(rootfile_path), cover_page_href)
                print("Path of cover page found: " + cover_page_path)
                # We try to find the <img> and get the "src" attribute:
                t = etree.fromstring(z.read(cover_page_path))
                cover_href = t.xpath("//xhtml:img", namespaces=namespaces)[0].get("src")
            except IndexError:
                pass

        if not cover_href:
            print("Cover image not found.")
            return None

        # In order to get the full path for the cover image,
        # we have to join rootfile_path and cover_href:
        cover_path = os.path.join(os.path.dirname(rootfile_path), cover_href)
        print("Path of cover image found: " + cover_path)

        # We return the image
        return cover_path