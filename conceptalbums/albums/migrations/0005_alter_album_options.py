# Generated by Django 4.0.3 on 2022-04-18 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0004_add_timestamps'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['pk']},
        ),
    ]