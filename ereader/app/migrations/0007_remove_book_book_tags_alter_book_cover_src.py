# Generated by Django 4.1.6 on 2023-05-25 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_book_folder_src_alter_book_book_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_tags',
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_src',
            field=models.FileField(null=True, upload_to='books/', verbose_name='Обладинка'),
        ),
    ]