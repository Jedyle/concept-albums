# Generated by Django 4.0.3 on 2022-04-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_album_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='tags',
            field=models.JSONField(null=True),
        ),
    ]