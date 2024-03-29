# Generated by Django 4.1.6 on 2023-02-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('description', models.TextField(verbose_name='Опис')),
                ('book_src', models.FileField(upload_to='asssets/books', verbose_name='Книга')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Час створення')),
                ('time_update', models.DateTimeField(auto_now_add=True, verbose_name='Час оновлення')),
                ('book_tags', models.ManyToManyField(to='app.category', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['id', '-time_create', 'title'],
            },
        ),
    ]
