# Generated by Django 2.1.7 on 2019-05-20 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0022_auto_20190520_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='AIM_GAMES.Tag', verbose_name='tags'),
        ),
    ]