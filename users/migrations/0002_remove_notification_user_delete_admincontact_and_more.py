# Generated by Django 4.2.16 on 2024-10-04 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdminContact',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]