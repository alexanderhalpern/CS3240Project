# Generated by Django 4.2.16 on 2024-11-02 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_file_description_file_keywords_file_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='title',
        ),
    ]
