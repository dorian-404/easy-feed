# Generated by Django 5.0.4 on 2024-05-11 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('easyFeed', '0008_alter_client_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='adresse',
        ),
        migrations.RemoveField(
            model_name='client',
            name='telephone',
        ),
    ]