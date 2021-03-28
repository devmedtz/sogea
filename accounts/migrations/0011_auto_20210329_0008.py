# Generated by Django 3.1.7 on 2021-03-28 21:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210317_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]