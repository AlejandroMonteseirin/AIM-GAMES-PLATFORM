# Generated by Django 2.1.7 on 2019-04-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0004_auto_20190425_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionmodel',
            name='price',
            field=models.FloatField(default=5, verbose_name='Price'),
            preserve_default=False,
        ),
    ]
