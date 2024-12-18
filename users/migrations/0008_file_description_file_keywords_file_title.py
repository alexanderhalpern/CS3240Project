# Generated by Django 4.2.16 on 2024-11-02 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_file_file_name_file_file_size_file_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
