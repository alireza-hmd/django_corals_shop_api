# Generated by Django 4.2 on 2023-05-06 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislikes_number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
