# Generated by Django 4.0.3 on 2022-04-18 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums_analyses', '0004_alter_albumanalysis_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likeanalysis',
            options={'verbose_name_plural': 'Likes'},
        ),
    ]
