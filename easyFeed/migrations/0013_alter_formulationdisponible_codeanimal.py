# Generated by Django 5.0.4 on 2024-05-15 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyFeed', '0012_merge_20240514_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulationdisponible',
            name='codeAnimal',
            field=models.CharField(max_length=3, unique=True),
        ),
    ]
