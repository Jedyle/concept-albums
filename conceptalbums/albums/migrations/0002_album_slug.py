# Generated by Django 4.0.3 on 2022-04-09 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
