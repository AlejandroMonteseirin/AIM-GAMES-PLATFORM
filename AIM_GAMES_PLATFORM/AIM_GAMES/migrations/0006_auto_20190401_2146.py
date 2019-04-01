# Generated by Django 2.1.7 on 2019-04-01 19:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AIM_GAMES', '0005_auto_20190329_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('objectives', models.TextField(verbose_name='objectives')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('user2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(verbose_name='location')),
                ('title', models.TextField(max_length=150, verbose_name='description')),
                ('description', models.TextField(verbose_name='description')),
                ('moment', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Chat', verbose_name='chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AlterField(
            model_name='aptitude',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AlterField(
            model_name='aptitude',
            name='title',
            field=models.TextField(max_length=30, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='business',
            name='lastPayment',
            field=models.DateTimeField(null=True, verbose_name='lastPayment'),
        ),
        migrations.AlterField(
            model_name='business',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Profile', verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='freelancer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Freelancer', verbose_name='freelancer'),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='verified'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='center',
            field=models.TextField(max_length=50, verbose_name='center'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='endDate',
            field=models.DateTimeField(verbose_name='endDate'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='formation',
            field=models.TextField(max_length=100, verbose_name='formation'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='miniature',
            field=models.URLField(verbose_name='miniature'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='startDate',
            field=models.DateTimeField(verbose_name='startDate'),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='profession',
            field=models.TextField(max_length=100, verbose_name='profession'),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Profile', verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='graphicengine',
            name='title',
            field=models.TextField(max_length=50, primary_key=True, serialize=False, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='graphicengineexperience',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AlterField(
            model_name='graphicengineexperience',
            name='graphicEngine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.GraphicEngine', verbose_name='graphicEngine'),
        ),
        migrations.AlterField(
            model_name='graphicengineexperience',
            name='graphicExperience',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='graphicExperience'),
        ),
        migrations.AlterField(
            model_name='html5showcase',
            name='curriculum',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='HTML5Showcase', to='AIM_GAMES.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AlterField(
            model_name='html5showcase',
            name='embedCode',
            field=models.TextField(verbose_name='embedCode'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Business', verbose_name='business'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='experienceRequired',
            field=models.TextField(max_length=100, verbose_name='experienceRequired'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='images',
            field=models.TextField(verbose_name='images'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='position',
            field=models.TextField(max_length=100, verbose_name='position'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='salary',
            field=models.IntegerField(verbose_name='salary'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='schedule',
            field=models.TextField(max_length=100, verbose_name='schedule'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='ubication',
            field=models.TextField(max_length=100, verbose_name='ubication'),
        ),
        migrations.AlterField(
            model_name='link',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='professionalexperience',
            name='center',
            field=models.TextField(max_length=50, verbose_name='center'),
        ),
        migrations.AlterField(
            model_name='professionalexperience',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AlterField(
            model_name='professionalexperience',
            name='endDate',
            field=models.DateTimeField(verbose_name='endDate'),
        ),
        migrations.AlterField(
            model_name='professionalexperience',
            name='formation',
            field=models.TextField(max_length=100, verbose_name='formation'),
        ),
        migrations.AlterField(
            model_name='professionalexperience',
            name='miniature',
            field=models.URLField(verbose_name='miniature'),
        ),
        migrations.AlterField(
            model_name='professionalexperience',
            name='startDate',
            field=models.DateTimeField(verbose_name='startDate'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.TextField(max_length=30, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dateOfBirth',
            field=models.DateTimeField(verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idCardNumber',
            field=models.TextField(max_length=10, verbose_name='IDCard Number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.TextField(max_length=30, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phoneNumber',
            field=models.TextField(max_length=20, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.URLField(verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='postalCode',
            field=models.TextField(max_length=16, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='surname',
            field=models.TextField(max_length=50, verbose_name='surname'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='response',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Business', verbose_name='business'),
        ),
        migrations.AlterField(
            model_name='response',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='response',
            name='pics',
            field=models.ManyToManyField(to='AIM_GAMES.URL', verbose_name='pics'),
        ),
        migrations.AlterField(
            model_name='response',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Thread', verbose_name='thread'),
        ),
        migrations.AlterField(
            model_name='response',
            name='title',
            field=models.TextField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.TextField(max_length=20, primary_key=True, serialize=False, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='attachedFiles',
            field=models.ManyToManyField(related_name='attachedFile', to='AIM_GAMES.URL', verbose_name='attachedFiles'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Business', verbose_name='business'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='pics',
            field=models.ManyToManyField(related_name='pic', to='AIM_GAMES.URL', verbose_name='pics'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(blank=True, to='AIM_GAMES.Tag', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.TextField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='url',
            name='title',
            field=models.URLField(verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='valoration',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Business', verbose_name='business'),
        ),
        migrations.AlterField(
            model_name='valoration',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='valoration',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Thread', verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='manager',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Profile', verbose_name='profile'),
        ),
        migrations.AddField(
            model_name='event',
            name='companies',
            field=models.ManyToManyField(to='AIM_GAMES.Business', verbose_name='companies'),
        ),
        migrations.AddField(
            model_name='event',
            name='freelancers',
            field=models.ManyToManyField(to='AIM_GAMES.Freelancer', verbose_name='freelancers'),
        ),
        migrations.AddField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Manager', verbose_name='manager'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIM_GAMES.Business', verbose_name='business'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='freelancers',
            field=models.ManyToManyField(to='AIM_GAMES.Freelancer', verbose_name='freelancers'),
        ),
    ]
