# Generated by Django 3.1.7 on 2021-04-04 23:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_customuser_is_moderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^\\S.*\\S$|^\\S$|^$', 'This field cannot start or end with spaces.')], verbose_name='Username'),
        ),
    ]
