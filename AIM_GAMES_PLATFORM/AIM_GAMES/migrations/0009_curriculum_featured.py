# Generated by Django 2.1.7 on 2019-04-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0008_auto_20190428_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
    ]