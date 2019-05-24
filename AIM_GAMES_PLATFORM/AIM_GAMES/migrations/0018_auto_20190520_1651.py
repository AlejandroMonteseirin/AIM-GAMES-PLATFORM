# Generated by Django 2.1.7 on 2019-05-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0017_event_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='companies',
            field=models.ManyToManyField(blank=True, to='AIM_GAMES.Business', verbose_name='companies'),
        ),
        migrations.AlterField(
            model_name='event',
            name='freelancers',
            field=models.ManyToManyField(blank=True, to='AIM_GAMES.Freelancer', verbose_name='freelancers'),
        ),
    ]