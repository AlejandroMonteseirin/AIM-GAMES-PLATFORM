# Generated by Django 2.1.7 on 2019-03-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(blank=True, to='AIM_GAMES.Tag'),
        ),
    ]