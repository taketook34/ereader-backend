# Generated by Django 4.1.6 on 2023-03-28 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_book_author_alter_book_book_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='folder_src',
            field=models.FileField(null=True, upload_to='', verbose_name='Папка для данних'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_tags',
            field=models.ManyToManyField(to='app.category', verbose_name='Теги'),
        ),
    ]