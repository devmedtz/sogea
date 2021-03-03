# Generated by Django 3.1.7 on 2021-03-02 08:27

from django.db import migrations, models
import django.utils.timezone
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_remove_post_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=posts.models.featured_image),
            preserve_default=False,
        ),
    ]
