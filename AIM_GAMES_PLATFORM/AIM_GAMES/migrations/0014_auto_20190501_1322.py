# Generated by Django 2.1.7 on 2019-05-01 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0013_auto_20190501_0211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemvariables',
            name='directPurchaseCoinsQuantity',
        ),
        migrations.AlterField(
            model_name='systemvariables',
            name='directPurchaseCoinsPrice',
            field=models.FloatField(default=3, verbose_name='Coins price'),
        ),
    ]
