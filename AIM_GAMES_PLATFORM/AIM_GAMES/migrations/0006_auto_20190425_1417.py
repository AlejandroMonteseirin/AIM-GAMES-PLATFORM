# Generated by Django 2.1.7 on 2019-04-25 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0005_subscriptionmodel_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='business',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='subscriptionModel',
        ),
        migrations.AddField(
            model_name='business',
            name='coins',
            field=models.IntegerField(default=0, verbose_name='Coins'),
        ),
        migrations.AddField(
            model_name='business',
            name='subscriptionModel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.SubscriptionModel'),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
