from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Book(models.Model):
    title = models.CharField(max_length=255, null=True, verbose_name="Назва")
    author = models.CharField(max_length=100, null=True, verbose_name="Автор")
    bookmark = models.IntegerField(default=0)
    #book_tags = models.ManyToManyField(Category, verbose_name="Теги")
    book_src = models.FileField(upload_to="books/", verbose_name="Книга")
    cover_src = models.FileField(upload_to="books/", null=True, verbose_name="Обладинка")
    folder_src = models.FileField(null=True, verbose_name="Папка для данних")
    #is_rendered = models.BooleanField(default=False, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    time_update = models.DateTimeField(auto_now_add=True, verbose_name="Час оновлення")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["id", "-time_create", "title"]



# Create your models here.
