# Generated by Django 2.1.7 on 2019-05-20 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0016_event_messageonjoin'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, to='AIM_GAMES.Tag', verbose_name='tags'),
        ),
    ]
