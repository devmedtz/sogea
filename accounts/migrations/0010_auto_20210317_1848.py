# Generated by Django 3.1.7 on 2021-03-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_profile_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_link',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook URL'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram_link',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram URL'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedin_link',
            field=models.URLField(blank=True, null=True, verbose_name='Linkedin URL'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='youtube_link',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube URL'),
        ),
    ]