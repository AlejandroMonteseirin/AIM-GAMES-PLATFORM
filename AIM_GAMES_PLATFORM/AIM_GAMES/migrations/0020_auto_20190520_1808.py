# Generated by Django 2.1.7 on 2019-05-20 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0019_auto_20190520_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, to='AIM_GAMES.Tag', verbose_name='tags'),
        ),
    ]
