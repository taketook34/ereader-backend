# Generated by Django 4.1.6 on 2023-03-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_book_is_rendered_alter_book_book_src_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.RemoveField(
            model_name='book',
            name='is_rendered',
        ),
        migrations.AlterField(
            model_name='book',
            name='book_src',
            field=models.FileField(upload_to='books/', verbose_name='Книга'),
        ),
    ]
