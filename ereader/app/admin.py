from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", 'book_src', "cover_src", "time_create")
    search_fields = ('title', 'author', 'time_update')
    list_editable = ('book_src', 'cover_src')

admin.site.register(Book, BookAdmin)
admin.site.register(Category)
# Register your models here.
