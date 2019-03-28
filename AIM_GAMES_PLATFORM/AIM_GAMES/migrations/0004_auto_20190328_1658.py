# Generated by Django 2.1.7 on 2019-03-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0003_professionalexperience_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professionalexperience',
            name='verified',
        ),
        migrations.AddField(
            model_name='curriculum',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
